from db.base import Base
from sqlalchemy import Column, TEXT, Integer, ForeignKey, Enum
import enum


class VisibilityStatus(enum.Enum):
    PRIVATE = "PRIVATE"
    PUBLIC = "PUBLIC"
    UNLISTED = "UNLISTED"


class ProcessingStatus(enum.Enum):
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    IN_PROGRESS = "IN_PROGRESS"


class Video(Base):
    __tablename__ = "videos"

    id = Column(TEXT, primary_key=True)
    title = Column(TEXT)
    description = Column(TEXT)
    user_id = Column(TEXT, ForeignKey("users.cognito_sub"))
    video_s3_key = Column(TEXT)
    # visibility = Column(
    #     Enum(VisibilityStatus),
    #     default=VisibilityStatus.PRIVATE,
    # )

    visibility = Column(
        Enum(
            VisibilityStatus,
            name="visibilitystatus", # The name of the type in PostgreSQL
            schema="public"         # Explicitly set the schema here
        ),
        nullable=False,
        default=VisibilityStatus.PRIVATE
    )
    
    is_processing = Column(
        Enum(ProcessingStatus),
        default=ProcessingStatus.IN_PROGRESS,
    )

    def to_dict(self):
        result = {}
        for c in self.__table__.columns:
            value = getattr(self, c.name)
            if isinstance(value, enum.Enum):
                value = value.value
            result[c.name] = value
        return result
