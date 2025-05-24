from pydantic import BaseModel, Field

class Node(BaseModel):
    name: str = Field(..., title="Name")
    


