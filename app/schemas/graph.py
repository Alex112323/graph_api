from pydantic import BaseModel, Field
from typing import List
from .node import Node
from .edge import Edge

class GraphCreate(BaseModel):
    nodes: List[Node] = Field(..., title="Nodes")
    edges: List[Edge] = Field(..., title="Edges")
    
class GraphCreateResponse(BaseModel):
    id: int = Field(..., title="ID of created graph")
    message: str | None = Field(None, title="Optional status message")

class GraphReadResponse(BaseModel):
    id: int = Field(..., title="Id")
    nodes: List[Node] = Field(..., title="Nodes")
    edges: List[Edge] = Field(..., title="Edges")
