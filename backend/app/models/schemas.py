from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field, field_validator

class TestCaseCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=1)
    instruction: str = Field(..., min_length=1, description="自然语言测试指令")
    start_url: Optional[str] = None
    tags: Optional[List[str]] = None

class TestCaseUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    instruction: Optional[str] = None
    start_url: Optional[str] = None
    tags: Optional[List[str]] = None

class TestCaseResponse(BaseModel):
    id: int
    name: str
    description: str
    instruction: str
    start_url: Optional[str] = None
    tags: Optional[List[str]] = None
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True

    @field_validator('created_at', 'updated_at', mode='before')
    @classmethod
    def convert_datetime(cls, v):
        if isinstance(v, datetime):
            return v.strftime('%Y-%m-%d %H:%M:%S')
        return str(v) if v else ''

class ExecutionRequest(BaseModel):
    test_case_id: int
    openai_api_key: Optional[str] = None
    headless: bool = True

class ExecutionResponse(BaseModel):
    id: int
    test_case_id: int
    status: str
    result: Optional[str] = None
    screenshots: List[str] = []
    logs: List[str] = []
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    error: Optional[str] = None

    class Config:
        from_attributes = True

    @field_validator('started_at', 'completed_at', mode='before')
    @classmethod
    def convert_datetime(cls, v):
        if isinstance(v, datetime):
            return v.strftime('%Y-%m-%d %H:%M:%S')
        return str(v) if v else None

class ActionRequest(BaseModel):
    action: str = Field(..., description="操作名称")
    parameters: dict = Field(default_factory=dict, description="操作参数")
    reasoning: str = Field(..., description="决策理由")

class SnapshotResponse(BaseModel):
    url: str
    title: str
    dom_snapshot: str
    timestamp: str

class ReportResponse(BaseModel):
    id: int
    test_case_id: int
    test_case_name: str
    status: str
    result: str
    screenshots: List[str]
    logs: List[str]
    duration_seconds: float
    created_at: str

    class Config:
        from_attributes = True

    @field_validator('created_at', mode='before')
    @classmethod
    def convert_datetime(cls, v):
        if isinstance(v, datetime):
            return v.strftime('%Y-%m-%d %H:%M:%S')
        return str(v) if v else ''
