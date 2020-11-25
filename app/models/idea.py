import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import column_property, relationship
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
    # id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4,
    #             unique=True, nullable=False)

    content = Column(String, index=True)
    impact = Column(Integer)
    ease = Column(Integer)
    confidence = Column(Integer)

    created_at: Column(DateTime(timezone=True), server_default=func.now())
    owner_id = Column(UUIDType, ForeignKey("user.id"))
    owner = relationship("User", back_populates="ideas")

    average_score = column_property((confidence + ease + impact) / 3)
