import uuid
from datetime import datetime, UTC
from typing import List, Optional, Dict
from src.domain.ports.video_repository import VideoRepository


class MockVideoRepository(VideoRepository):
    def __init__(self):
        self.videos = {}
        self.next_id = 1
    
    def save(self, video):
        # Generate an ID if not present
        if not video.id:
            video.id = f"test-video-{self.next_id}"
            self.next_id += 1
        
        # Save to dictionary
        self.videos[video.id] = video
        return video
    
    def update(self, video):
        # Update existing video
        if video.id in self.videos:
            self.videos[video.id] = video
        return video
    
    def get_by_id(self, video_id):
        # Return video if exists
        return self.videos.get(video_id)
    
    def list_all(self):
        # Return all videos
        return list(self.videos.values())
from src.domain.models.video import Video
from src.domain.ports.video_repository import VideoRepository


class MockVideoRepository(VideoRepository):
    """
    A mock implementation of the VideoRepository for testing purposes.
    This avoids database dependencies in tests.
    """
    
    def __init__(self):
        """Initialize an empty repository"""
        self.videos: Dict[str, Video] = {}
    
    def save(self, video: Video) -> Video:
        """
        Save a video to the mock repository.
        
        Args:
            video: The video to save
            
        Returns:
            The saved video with an ID
        """
        # Generate an ID if none exists
        if not video.id:
            video.id = str(uuid.uuid4())
        
        # Make a copy to avoid reference issues
        saved_video = Video(
            id=video.id,
            filename=video.filename,
            gcs_url=video.gcs_url,
            status=video.status,
            analysis_result=video.analysis_result,
            created_at=video.created_at,
            updated_at=video.updated_at
        )
        
        self.videos[saved_video.id] = saved_video
        return saved_video
    
    def update(self, video: Video) -> Video:
        """
        Update a video in the mock repository.
        
        Args:
            video: The video to update
            
        Returns:
            The updated video
            
        Raises:
            ValueError: If the video doesn't exist
        """
        if not video.id or video.id not in self.videos:
            raise ValueError(f"Video with ID {video.id} not found")
        
        # Update the existing video
        self.videos[video.id] = Video(
            id=video.id,
            filename=video.filename,
            gcs_url=video.gcs_url,
            status=video.status,
            analysis_result=video.analysis_result,
            created_at=video.created_at,
            updated_at=datetime.now(UTC)  # Update the updated_at timestamp
        )
        
        return self.videos[video.id]
    
    def get_by_id(self, video_id: str) -> Optional[Video]:
        """
        Get a video by ID from the mock repository.
        
        Args:
            video_id: The ID of the video
            
        Returns:
            The video if found, None otherwise
        """
        return self.videos.get(video_id)
    
    def list_all(self) -> List[Video]:
        """
        List all videos in the mock repository.
        
        Returns:
            A list of all videos
        """
        return list(self.videos.values())
