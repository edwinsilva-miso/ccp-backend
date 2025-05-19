import pytest
from src.domain.models.video import VideoStatus


class TestVideoStatus:
    def test_video_status_values(self):
        """Test that VideoStatus has the expected values"""
        assert VideoStatus.UPLOADED.value == "UPLOADED"
        assert VideoStatus.PROCESSING.value == "PROCESSING"
        assert VideoStatus.COMPLETED.value == "COMPLETED"
        assert VideoStatus.FAILED.value == "FAILED"
    
    def test_video_status_comparison(self):
        """Test that VideoStatus can be compared directly"""
        status = VideoStatus.UPLOADED
        
        assert status == VideoStatus.UPLOADED
        assert status != VideoStatus.PROCESSING
        assert status != VideoStatus.COMPLETED
        assert status != VideoStatus.FAILED
