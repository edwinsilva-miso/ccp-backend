from enum import Enum
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


class VideoStatus(Enum):
    UPLOADED = "UPLOADED"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


@dataclass
class Video:
    id: Optional[str] = None
    filename: str = ""
    gcs_url: str = ""
    status: VideoStatus = VideoStatus.UPLOADED
    analysis_result: Optional[str] = None
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()
