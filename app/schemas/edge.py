from pydantic import BaseModel, Field

class Edge(BaseModel):
    source: str = Field(..., title="Source")
    target: str = Field(..., title="Target")
