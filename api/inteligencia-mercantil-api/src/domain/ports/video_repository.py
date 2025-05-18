from abc import ABC, abstractmethod
from typing import Optional, List
from src.domain.models.video import Video


class VideoRepository(ABC):
    @abstractmethod
    def save(self, video: Video) -> Video:
        """Save a video to the repository"""
        pass
    
    @abstractmethod
    def get_by_id(self, video_id: str) -> Optional[Video]:
        """Get a video by its ID"""
        pass
    
    @abstractmethod
    def update(self, video: Video) -> Video:
        """Update a video in the repository"""
        pass
    
    @abstractmethod
    def list_all(self) -> List[Video]:
        """List all videos in the repository"""
        pass
