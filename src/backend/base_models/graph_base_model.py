from pydantic import BaseModel, Field
from datetime import datetime

class GraphBase(BaseModel):
    graphId: int = Field(gt=0)
    userIdFK: int = Field(gt=0)
    graphName: str = Field(min_length=2, max_length=16)
    fileName: str = Field(min_length=2, max_length=16)
    createDate: datetime