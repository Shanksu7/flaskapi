from typing import Generic, TypeVar, Optional
from pydantic import BaseModel

T = TypeVar('T')

class ApiResponse(BaseModel, Generic[T]):
    error: bool
    data: Optional[T] = None
    message: Optional[str] = None
    status: str
