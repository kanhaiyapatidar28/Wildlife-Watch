from typing import Generic, TypeVar, Optional, Any, Dict, List
from pydantic import BaseModel, Field
from datetime import datetime, timezone

T = TypeVar("T")


class ResponseMeta(BaseModel):
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    request_id: Optional[str] = None
    total_count: Optional[int] = None


class StandardResponse(BaseModel, Generic[T]):
    success: bool = True
    data: T
    meta: ResponseMeta = Field(default_factory=ResponseMeta)


class ErrorDetail(BaseModel):
    field: Optional[str] = None
    message: str


class ProblemDetails(BaseModel):
    type: str = "https://errors.wildlifewatch.org/problem"
    title: str
    status: int
    detail: str
    instance: Optional[str] = None
    errors: Optional[List[ErrorDetail]] = None
