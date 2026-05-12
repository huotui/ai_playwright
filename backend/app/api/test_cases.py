from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.database import get_db
from app.models.schemas import TestCaseCreate, TestCaseUpdate, TestCaseResponse
from app.services.test_service import TestCaseService
from datetime import datetime

router = APIRouter(prefix="/api/test-cases", tags=["测试用例"])

@router.post("/", response_model=TestCaseResponse)
def create_test_case(test_case: TestCaseCreate, db: Session = Depends(get_db)):
    return TestCaseService.create_test_case(db, test_case)

@router.get("/", response_model=List[TestCaseResponse])
def get_test_cases(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return TestCaseService.get_test_cases(db, skip, limit)

@router.get("/{test_case_id}", response_model=TestCaseResponse)
def get_test_case(test_case_id: int, db: Session = Depends(get_db)):
    test_case = TestCaseService.get_test_case(db, test_case_id)
    if not test_case:
        raise HTTPException(status_code=404, detail="测试用例不存在")
    return test_case

@router.put("/{test_case_id}", response_model=TestCaseResponse)
def update_test_case(test_case_id: int, test_case: TestCaseUpdate, db: Session = Depends(get_db)):
    updated_test_case = TestCaseService.update_test_case(db, test_case_id, test_case)
    if not updated_test_case:
        raise HTTPException(status_code=404, detail="测试用例不存在")
    return updated_test_case

@router.delete("/{test_case_id}")
def delete_test_case(test_case_id: int, db: Session = Depends(get_db)):
    success = TestCaseService.delete_test_case(db, test_case_id)
    if not success:
        raise HTTPException(status_code=404, detail="测试用例不存在")
    return {"message": "测试用例已删除"}
