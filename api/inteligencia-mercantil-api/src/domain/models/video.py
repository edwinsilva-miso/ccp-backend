from enum import Enum
from dataclasses import dataclass
from typing import Optional
from datetime import datetime, UTC


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
    created_at: datetime = datetime.now(UTC)
    updated_at: datetime = datetime.now(UTC)

