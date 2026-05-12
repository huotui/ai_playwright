from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.models.database import get_db, TestCase, TestExecution
from app.models.schemas import ReportResponse
from app.services.test_service import TestExecutionService
from datetime import datetime

router = APIRouter(prefix="/api/reports", tags=["测试报告"])

@router.get("/{execution_id}", response_model=ReportResponse)
def get_report(execution_id: int, db: Session = Depends(get_db)):
    execution = TestExecutionService.get_execution(db, execution_id)
    if not execution:
        raise HTTPException(status_code=404, detail="测试报告不存在")
    
    test_case = db.query(TestCase).filter(TestCase.id == execution.test_case_id).first()
    
    duration = 0
    if execution.started_at and execution.completed_at:
        duration = (execution.completed_at - execution.started_at).total_seconds()
    
    return ReportResponse(
        id=execution.id,
        test_case_id=execution.test_case_id,
        test_case_name=test_case.name if test_case else "Unknown",
        status=execution.status,
        result=execution.result or "",
        screenshots=execution.screenshots or [],
        logs=execution.logs or [],
        duration_seconds=duration,
        created_at=str(execution.created_at)
    )

@router.get("/", response_model=List[ReportResponse])
def get_reports(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    executions = TestExecutionService.get_executions(db, skip=skip, limit=limit)
    reports = []
    for execution in executions:
        test_case = db.query(TestCase).filter(TestCase.id == execution.test_case_id).first()
        duration = 0
        if execution.started_at and execution.completed_at:
            duration = (execution.completed_at - execution.started_at).total_seconds()
        
        reports.append(ReportResponse(
            id=execution.id,
            test_case_id=execution.test_case_id,
            test_case_name=test_case.name if test_case else "Unknown",
            status=execution.status,
            result=execution.result or "",
            screenshots=execution.screenshots or [],
            logs=execution.logs or [],
            duration_seconds=duration,
            created_at=str(execution.created_at)
        ))
    return reports
