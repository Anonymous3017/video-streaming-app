from db.base import Base
from sqlalchemy import Column, TEXT, ForeignKey, Enum
from enum import Enum


class VisibilityStatus(Enum):
    PUBLIC = "PUBLIC"
    PRIVATE = "PRIVATE"
    UNLISTED = "UNLISTED"


class ProcessingStatus(Enum):
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class Video(Base):
    __tablename__ = "videos"

    id = Column(TEXT, primary_key=True)
    title = Column(TEXT, nullable=False)
    description = Column(TEXT)
    user_id = Column(TEXT, ForeignKey("users.id"), nullable=False)
    video_s3_key = Column(TEXT, nullable=False)
    visibility = Column(
        Enum(VisibilityStatus),
        nullable=False,
        default=VisibilityStatus.PRIVATE,
    )
    is_processing = Column(
        Enum(ProcessingStatus),
        nullable=False,
        default=ProcessingStatus.IN_PROGRESS,
    )
