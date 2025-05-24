from pydantic import BaseModel, Field
from typing import List, Dict

class ErrorResponse(BaseModel):
    message: str = Field(..., title="Message")

class ValidationError(BaseModel):
    loc: List[str] = Field(..., title="Location")
    msg: str = Field(..., title="Message")
    type: str = Field(..., title="Error Type")

class HTTPValidationError(BaseModel):
    detail: List[ValidationError] = Field(default_factory=list, title="Detail")
    
AdjacencyListResponse = Dict[str, List[str]]
