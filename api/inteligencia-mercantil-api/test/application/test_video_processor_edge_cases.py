import pytest
from unittest.mock import Mock, patch
from datetime import datetime

from src.application.use_cases.video_processor import VideoProcessor
from src.domain.models.video import Video, VideoStatus


class TestVideoProcessorEdgeCases:
    @pytest.fixture
    def processor_components(self):
        """Create mocked components for the VideoProcessor"""
        mock_repository = Mock()
        mock_storage = Mock()
        mock_analyzer = Mock()
        
        return mock_repository, mock_storage, mock_analyzer
    
    @pytest.fixture
    def processor(self, processor_components):
        """Create a VideoProcessor with mocked components"""
        mock_repository, mock_storage, mock_analyzer = processor_components
        return VideoProcessor(mock_repository, mock_storage, mock_analyzer)
    
    def test_process_video_with_none_result(self, processor, processor_components):
        """Test processing a video when analyzer returns None"""
        # Arrange
        mock_repository, _, mock_analyzer = processor_components
        video_id = "test-id"
        
        # Configure mock repository to return a test video
        test_video = Video(
            id=video_id,
            filename="test.mp4",
            gcs_url="gs://test-bucket/test.mp4",
            status=VideoStatus.UPLOADED
        )
        mock_repository.get_by_id.return_value = test_video
        
        # Configure analyzer to return None
        mock_analyzer.analyze_video.return_value = None
        
        # Act
        processor.process_video(video_id)
        
        # Assert
        mock_repository.update.assert_called()
        
        # Get the updated video from the last call
        updated_video = mock_repository.update.call_args_list[-1][0][0]
        assert updated_video.status == VideoStatus.FAILED
        assert updated_video.analysis_result is None
    
    def test_process_video_non_existent(self, processor, processor_components):
        """Test processing a video that doesn't exist"""
        # Arrange
        mock_repository, _, _ = processor_components
        video_id = "non-existent-id"
        
        # Configure repository to return None
        mock_repository.get_by_id.return_value = None
        
        # Act
        processor.process_video(video_id)
        
        # Assert
        mock_repository.get_by_id.assert_called_once_with(video_id)
        mock_repository.update.assert_not_called()
    
    def test_process_video_async_without_flask_context(self, processor):
        """Test async processing outside of a Flask context"""
        # Arrange
        video_id = "test-id"
        
        # Act - simulate being outside a Flask context by raising RuntimeError
        with patch('flask.current_app._get_current_object', side_effect=RuntimeError("No Flask context")), \
             patch('threading.Thread') as mock_thread:
            
            processor._process_video_async(video_id)
            
            # Assert
            mock_thread.assert_called_once()
            # Check that the thread was given the correct function and arguments
            args, kwargs = mock_thread.call_args
            assert kwargs['target'] == processor.process_video
            assert kwargs['args'] == (video_id,)
            assert kwargs['daemon'] is True
