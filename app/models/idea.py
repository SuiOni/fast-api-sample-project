import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy_utils import UUIDType

from app.db.base_class import Base

if TYPE_CHECKING:
    from .user import User  # noqa: F401


class Idea(Base):
    id = Column(
        UUIDType,
        primary_key=True,
        index=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )

    content = Column(String, index=True)
    impact = Column(Integer)
    ease = Column(Integer)
    confidence = Column(Integer)
    timestamp = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    owner_id = Column(UUIDType, ForeignKey("user.id"))
    owner = relationship("User", back_populates="ideas")

    @hybrid_property
    def created_at(self):
        self.timestamp
        print(self.timestamp.timestamp())
        return self.timestamp.timestamp()

    @hybrid_property
    def average_score(self):
        avg = (self.confidence + self.ease + self.impact) / 3.0
        print("avg", avg, self.created_at)
        return avg
