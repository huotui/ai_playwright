from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.database import TestCase, TestExecution
from app.models.schemas import TestCaseCreate, TestCaseUpdate

class TestCaseService:
    
    @staticmethod
    def create_test_case(db: Session, test_case: TestCaseCreate) -> TestCase:
        db_test_case = TestCase(
            name=test_case.name,
            description=test_case.description,
            instruction=test_case.instruction,
            start_url=test_case.start_url,
            tags=test_case.tags or []
        )
        db.add(db_test_case)
        db.commit()
        db.refresh(db_test_case)
        return db_test_case

    @staticmethod
    def get_test_case(db: Session, test_case_id: int) -> Optional[TestCase]:
        return db.query(TestCase).filter(TestCase.id == test_case_id).first()

    @staticmethod
    def get_test_cases(db: Session, skip: int = 0, limit: int = 100) -> List[TestCase]:
        return db.query(TestCase).offset(skip).limit(limit).all()

    @staticmethod
    def update_test_case(db: Session, test_case_id: int, test_case: TestCaseUpdate) -> Optional[TestCase]:
        db_test_case = db.query(TestCase).filter(TestCase.id == test_case_id).first()
        if not db_test_case:
            return None
        
        update_data = test_case.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_test_case, field, value)
        
        db.commit()
        db.refresh(db_test_case)
        return db_test_case

    @staticmethod
    def delete_test_case(db: Session, test_case_id: int) -> bool:
        db_test_case = db.query(TestCase).filter(TestCase.id == test_case_id).first()
        if not db_test_case:
            return False
        
        db.delete(db_test_case)
        db.commit()
        return True


class TestExecutionService:
    
    @staticmethod
    def create_execution(db: Session, test_case_id: int) -> TestExecution:
        execution = TestExecution(
            test_case_id=test_case_id,
            status="pending"
        )
        db.add(execution)
        db.commit()
        db.refresh(execution)
        return execution

    @staticmethod
    def update_execution(db: Session, execution_id: int, **kwargs) -> Optional[TestExecution]:
        execution = db.query(TestExecution).filter(TestExecution.id == execution_id).first()
        if not execution:
            return None
        
        for field, value in kwargs.items():
            setattr(execution, field, value)
        
        db.commit()
        db.refresh(execution)
        return execution

    @staticmethod
    def get_execution(db: Session, execution_id: int) -> Optional[TestExecution]:
        return db.query(TestExecution).filter(TestExecution.id == execution_id).first()

    @staticmethod
    def get_executions(db: Session, test_case_id: Optional[int] = None, skip: int = 0, limit: int = 100) -> List[TestExecution]:
        query = db.query(TestExecution)
        if test_case_id:
            query = query.filter(TestExecution.test_case_id == test_case_id)
        return query.order_by(TestExecution.created_at.desc()).offset(skip).limit(limit).all()
