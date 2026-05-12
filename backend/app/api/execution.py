from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.database import get_db, TestExecution, TestCase
from app.models.schemas import ExecutionRequest, ExecutionResponse, ReportResponse
from app.services.test_service import TestExecutionService, TestCaseService
from app.core.agent import AITestAgent
from app.core.playwright_mcp import PlaywrightMCP
from app.config import settings
from datetime import datetime
import asyncio
import json
import threading

router = APIRouter(prefix="/api/execution", tags=["测试执行"])

execution_tasks = {}

@router.post("/start", response_model=ExecutionResponse)
async def start_execution(request: ExecutionRequest, db: Session = Depends(get_db)):
    test_case = TestCaseService.get_test_case(db, request.test_case_id)
    if not test_case:
        raise HTTPException(status_code=404, detail="测试用例不存在")

    execution = TestExecutionService.create_execution(db, request.test_case_id)
    start_time = datetime.utcnow()
    
    TestExecutionService.update_execution(db, execution.id, status="running", started_at=start_time)
    
    thread = threading.Thread(
        target=run_test,
        args=(execution.id, request.test_case_id, request.openai_api_key),
        daemon=True
    )
    thread.start()
    execution_tasks[execution.id] = thread
    
    return ExecutionResponse(
        id=execution.id,
        test_case_id=execution.test_case_id,
        status="running"
    )

@router.get("/{execution_id}", response_model=ExecutionResponse)
def get_execution(execution_id: int, db: Session = Depends(get_db)):
    execution = TestExecutionService.get_execution(db, execution_id)
    if not execution:
        raise HTTPException(status_code=404, detail="测试执行不存在")
    
    return ExecutionResponse(
        id=execution.id,
        test_case_id=execution.test_case_id,
        status=execution.status,
        result=execution.result,
        logs=execution.logs or [],
        completed_at=str(execution.completed_at) if execution.completed_at else None,
        error=execution.error
    )

@router.get("/", response_model=List[ExecutionResponse])
def get_executions(test_case_id: Optional[int] = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    executions = TestExecutionService.get_executions(db, test_case_id, skip, limit)
    return [
        ExecutionResponse(
            id=e.id,
            test_case_id=e.test_case_id,
            status=e.status,
            result=e.result,
            logs=e.logs or [],
            completed_at=str(e.completed_at) if e.completed_at else None,
            error=e.error
        )
        for e in executions
    ]

def run_test(execution_id: int, test_case_id: int, openai_api_key: str):
    from app.models.database import SessionLocal
    from playwright.sync_api import sync_playwright
    
    start_time = datetime.utcnow()
    session_id = f"exec_{execution_id}"
    
    db = SessionLocal()
    playwright = None
    browser = None
    context = None
    page = None
    
    try:
        test_case = db.query(TestCase).filter(TestCase.id == test_case_id).first()
        if not test_case:
            TestExecutionService.update_execution(
                db, execution_id,
                status="failed",
                error="测试用例不存在",
                completed_at=datetime.utcnow()
            )
            return
        
        playwright = sync_playwright().start()
        browser = playwright.chromium.launch(headless=settings.HEADLESS)
        context = browser.new_context(
            viewport={"width": settings.VIEWPORT_WIDTH, "height": settings.VIEWPORT_HEIGHT}
        )
        page = context.new_page()
        mcp = PlaywrightMCP(page)
        agent = AITestAgent(api_key=openai_api_key)
        
        instruction = test_case.instruction
        if test_case.start_url:
            instruction = f"首先导航到 {test_case.start_url}，然后{instruction}"
        
        result = agent.execute_test(instruction, mcp)
        
        end_time = datetime.utcnow()
        duration = (end_time - start_time).total_seconds()
        
        if result["success"]:
            TestExecutionService.update_execution(
                db, execution_id,
                status="completed",
                result=result["result"],
                logs=result["logs"],
                completed_at=end_time,
                duration_seconds=duration
            )
        else:
            TestExecutionService.update_execution(
                db, execution_id,
                status="failed",
                result=result["result"],
                logs=result["logs"],
                error=result.get("result"),
                completed_at=end_time,
                duration_seconds=duration
            )
        
    except Exception as e:
        end_time = datetime.utcnow()
        duration = (end_time - start_time).total_seconds()
        TestExecutionService.update_execution(
            db, execution_id,
            status="failed",
            error=str(e),
            completed_at=end_time,
            duration_seconds=duration
        )
    finally:
        if context:
            context.close()
        if browser:
            browser.close()
        if playwright:
            playwright.stop()
        db.close()
