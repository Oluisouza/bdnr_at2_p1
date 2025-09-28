from pydantic import BaseModel, Field
from datetime import datetime

class MessageIn(BaseModel):
    user: str = Field(..., max_length=50)
    message: str = Field(..., min_length=1, max_length=1000)

class MessageOut(BaseModel):
    id: str
    room: str
    username: str
    content: str
    created_at: datetime