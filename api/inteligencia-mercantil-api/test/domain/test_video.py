import pytest
from datetime import datetime
from src.domain.models.video import Video, VideoStatus


class TestVideo:
    def test_video_initialization(self):
        """Test that Video can be initialized with default values"""
        video = Video()
        
        assert video.id is None
        assert video.filename == ""
        assert video.gcs_url == ""
        assert video.status == VideoStatus.UPLOADED
        assert video.analysis_result is None
        assert isinstance(video.created_at, datetime)
        assert isinstance(video.updated_at, datetime)
    
    def test_video_initialization_with_custom_values(self):
        """Test that Video can be initialized with custom values"""
        created_at = datetime.utcnow()
        updated_at = datetime.utcnow()
        
        video = Video(
            id="123",
            filename="test.mp4",
            gcs_url="gs://bucket/test.mp4",
            status=VideoStatus.PROCESSING,
            analysis_result="Sample analysis",
            created_at=created_at,
            updated_at=updated_at
        )
        
        assert video.id == "123"
        assert video.filename == "test.mp4"
        assert video.gcs_url == "gs://bucket/test.mp4"
        assert video.status == VideoStatus.PROCESSING
        assert video.analysis_result == "Sample analysis"
        assert video.created_at == created_at
        assert video.updated_at == updated_at
