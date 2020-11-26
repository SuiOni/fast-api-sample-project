from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, validator


# Shared properties
class IdeaBase(BaseModel):
    content: Optional[str] = None
    impact: Optional[int] = None
    ease: Optional[int] = None
    confidence: Optional[int] = None

    @validator("impact", "ease", "confidence")
    def max_value_10(cls, value: int):
        if value > 10 or value < 1:
            raise ValueError("must be between 1 and 10 included")
        return value


# Properties to receive on idea creation
class IdeaCreate(IdeaBase):
    content: str
    impact: int
    ease: int
    confidence: int


# Properties to receive on idea update
class IdeaUpdate(IdeaBase):
    pass


# Properties shared by models stored in DB
class IdeaInDBBase(IdeaBase):
    id: UUID
    content: str
    impact: int
    ease: int
    confidence: int
    average_score: float
    created_at: int

    class Config:
        orm_mode = True


# Properties to return to client
class Idea(IdeaInDBBase):
    pass


# Properties properties stored in DB
class IdeaInDB(IdeaInDBBase):
    owner_id: int
    timestamp: datetime
