import pytest
from unittest.mock import Mock, patch
from datetime import datetime
from io import BytesIO

from src.domain.models.video import Video, VideoStatus
from src.application.use_cases.video_processor import VideoProcessor


class TestVideoProcessor:
    @pytest.fixture
    def mock_repository(self):
        repository = Mock()
        # Setup save to return a video with ID
        repository.save.side_effect = lambda video: Video(
            id="test-id",
            filename=video.filename,
            gcs_url=video.gcs_url,
            status=video.status,
            created_at=video.created_at,
            updated_at=video.updated_at
        )
        return repository
    
    @pytest.fixture
    def mock_storage(self):
        storage = Mock()
        storage.upload_file.return_value = "gs://test-bucket/test.mp4"
        storage.get_file_url.return_value = "gs://test-bucket/test.mp4"
        return storage
    
    @pytest.fixture
    def mock_analyzer(self):
        analyzer = Mock()
        analyzer.analyze_video.return_value = "Test analysis result"
        return analyzer
    
    @pytest.fixture
    def processor(self, mock_repository, mock_storage, mock_analyzer):
        return VideoProcessor(
            video_repository=mock_repository,
            storage_service=mock_storage,
            analyzer_service=mock_analyzer
        )
    
    def test_upload_video(self, processor, mock_storage, mock_repository):
        """Test that upload_video uploads the file and saves a video entity"""
        # Arrange
        file_data = BytesIO(b"test video content")
        filename = "test.mp4"
        
        # Act
        with patch('threading.Thread') as mock_thread:
            result = processor.upload_video(file_data, filename)
        
        # Assert
        mock_storage.upload_file.assert_called_once_with(file_data, filename)
        mock_repository.save.assert_called_once()
        assert mock_thread.called
        assert result.id == "test-id"
        assert result.filename == filename
        assert result.gcs_url == "gs://test-bucket/test.mp4"
        assert result.status == VideoStatus.UPLOADED
    
    def test_process_video_success(self, processor, mock_repository, mock_analyzer):
        """Test that process_video processes a video successfully"""
        # Arrange
        video_id = "test-id"
        video = Video(
            id=video_id,
            filename="test.mp4",
            gcs_url="gs://test-bucket/test.mp4",
            status=VideoStatus.UPLOADED
        )
        mock_repository.get_by_id.return_value = video
        
        # Act
        processor.process_video(video_id)
        
        # Assert
        mock_repository.get_by_id.assert_called_once_with(video_id)
        mock_analyzer.analyze_video.assert_called_once_with(video.gcs_url)
        
        # Check that repository.update was called twice
        assert mock_repository.update.call_count == 2
        
        # Get the second call's arguments (the final update)
        updated_video = mock_repository.update.call_args_list[1][0][0]
        assert updated_video.status == VideoStatus.COMPLETED
        assert updated_video.analysis_result == "Test analysis result"
    
    def test_process_video_failure(self, processor, mock_repository, mock_analyzer):
        """Test that process_video handles errors properly"""
        # Arrange
        video_id = "test-id"
        video = Video(
            id=video_id,
            filename="test.mp4",
            gcs_url="gs://test-bucket/test.mp4",
            status=VideoStatus.UPLOADED
        )
        mock_repository.get_by_id.return_value = video
        mock_analyzer.analyze_video.side_effect = Exception("Test error")
        
        # Act
        processor.process_video(video_id)
        
        # Assert
        mock_repository.get_by_id.assert_called_once_with(video_id)
        mock_analyzer.analyze_video.assert_called_once_with(video.gcs_url)
        
        # Check that repository.update was called twice
        assert mock_repository.update.call_count == 2
        
        # Get the second call's arguments (the final update)
        updated_video = mock_repository.update.call_args_list[1][0][0]
        assert updated_video.status == VideoStatus.FAILED
        assert "Error analyzing video: Test error" in updated_video.analysis_result
    
    def test_process_video_not_found(self, processor, mock_repository):
        """Test that process_video handles non-existent videos properly"""
        # Arrange
        video_id = "non-existent-id"
        mock_repository.get_by_id.return_value = None
        
        # Act
        processor.process_video(video_id)
        
        # Assert
        mock_repository.get_by_id.assert_called_once_with(video_id)
        mock_repository.update.assert_not_called()
    
    def test_get_video_status(self, processor, mock_repository):
        """Test that get_video_status returns the correct video"""
        # Arrange
        video_id = "test-id"
        video = Video(id=video_id)
        mock_repository.get_by_id.return_value = video
        
        # Act
        result = processor.get_video_status(video_id)
        
        # Assert
        mock_repository.get_by_id.assert_called_once_with(video_id)
        assert result == video
    
    def test_process_video_async(self, processor):
        """Test that _process_video_async starts a thread"""
        # Arrange
        video_id = "test-id"
        
        # Act
        with patch('threading.Thread') as mock_thread:
            instance = mock_thread.return_value
            processor._process_video_async(video_id)
        
        # Assert
        mock_thread.assert_called_once()
        instance.start.assert_called_once()
