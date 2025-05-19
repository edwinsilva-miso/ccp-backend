import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime
import uuid

from src.domain.models.video import Video, VideoStatus
from src.infrastructure.adapters.sqlalchemy_video_repository import SQLAlchemyVideoRepository
from src.infrastructure.database.models import VideoModel


@pytest.mark.skip
class TestSQLAlchemyVideoRepository:
    @pytest.fixture
    def mock_db_session(self):
        """Create a mock for the database session"""
        with patch('src.infrastructure.adapters.sqlalchemy_video_repository.db.session') as mock_session:
            yield mock_session
    
    @pytest.fixture
    def repository(self, mock_db_session):
        return SQLAlchemyVideoRepository()
    
    def test_save_new_video(self, repository, mock_db_session):
        """Test saving a new video entity"""
        # Arrange
        video = Video(
            filename="test.mp4",
            gcs_url="gs://test-bucket/test.mp4",
            status=VideoStatus.UPLOADED
        )
        
        # Configure mock to add an ID when add is called
        def add_side_effect(model):
            model.id = str(uuid.uuid4())
        
        mock_db_session.add.side_effect = add_side_effect
        
        # Act
        result = repository.save(video)
        
        # Assert
        mock_db_session.add.assert_called_once()
        mock_db_session.commit.assert_called_once()
        assert result.id is not None
        assert result.filename == "test.mp4"
        assert result.gcs_url == "gs://test-bucket/test.mp4"
        assert result.status == VideoStatus.UPLOADED
    
    def test_update_video(self, repository, mock_db_session):
        """Test updating an existing video entity"""
        # Arrange
        video_id = str(uuid.uuid4())
        video = Video(
            id=video_id,
            filename="test.mp4",
            gcs_url="gs://test-bucket/test.mp4",
            status=VideoStatus.PROCESSING,
            analysis_result="Test analysis"
        )
        
        # Mock the existing model in the database
        mock_model = MagicMock()
        mock_db_session.query.return_value.filter_by.return_value.first.return_value = mock_model
        
        # Act
        result = repository.update(video)
        
        # Assert
        mock_db_session.query.assert_called_once_with(VideoModel)
        mock_db_session.query.return_value.filter_by.assert_called_once_with(id=video_id)
        mock_db_session.commit.assert_called_once()
        
        # Check that model attributes were updated
        assert mock_model.filename == "test.mp4"
        assert mock_model.gcs_url == "gs://test-bucket/test.mp4"
        assert mock_model.status == VideoStatus.PROCESSING.value
        assert mock_model.analysis_result == "Test analysis"
        
        # Check that return is correct
        assert result.id == video_id
        assert result.filename == "test.mp4"
        assert result.status == VideoStatus.PROCESSING
    
    def test_get_by_id_found(self, repository, mock_db_session):
        """Test getting a video by ID when it exists"""
        # Arrange
        video_id = str(uuid.uuid4())
        created_at = datetime.utcnow()
        updated_at = datetime.utcnow()
        
        # Mock database model
        mock_model = MagicMock()
        mock_model.id = video_id
        mock_model.filename = "test.mp4"
        mock_model.gcs_url = "gs://test-bucket/test.mp4"
        mock_model.status = VideoStatus.COMPLETED.value
        mock_model.analysis_result = "Test analysis"
        mock_model.created_at = created_at
        mock_model.updated_at = updated_at
        
        mock_db_session.query.return_value.filter_by.return_value.first.return_value = mock_model
        
        # Act
        result = repository.get_by_id(video_id)
        
        # Assert
        mock_db_session.query.assert_called_once_with(VideoModel)
        mock_db_session.query.return_value.filter_by.assert_called_once_with(id=video_id)
        
        assert result.id == video_id
        assert result.filename == "test.mp4"
        assert result.gcs_url == "gs://test-bucket/test.mp4"
        assert result.status == VideoStatus.COMPLETED
        assert result.analysis_result == "Test analysis"
        assert result.created_at == created_at
        assert result.updated_at == updated_at
    
    def test_get_by_id_not_found(self, repository, mock_db_session):
        """Test getting a video by ID when it doesn't exist"""
        # Arrange
        video_id = str(uuid.uuid4())
        mock_db_session.query.return_value.filter_by.return_value.first.return_value = None
        
        # Act
        result = repository.get_by_id(video_id)
        
        # Assert
        mock_db_session.query.assert_called_once_with(VideoModel)
        mock_db_session.query.return_value.filter_by.assert_called_once_with(id=video_id)
        assert result is None
    
    def test_list_all(self, repository, mock_db_session):
        """Test listing all videos"""
        # Arrange
        video_id1 = str(uuid.uuid4())
        video_id2 = str(uuid.uuid4())
        
        # Mock database models
        mock_model1 = MagicMock()
        mock_model1.id = video_id1
        mock_model1.filename = "test1.mp4"
        mock_model1.status = VideoStatus.COMPLETED.value
        
        mock_model2 = MagicMock()
        mock_model2.id = video_id2
        mock_model2.filename = "test2.mp4"
        mock_model2.status = VideoStatus.PROCESSING.value
        
        mock_db_session.query.return_value.all.return_value = [mock_model1, mock_model2]
        
        # Act
        result = repository.list_all()
        
        # Assert
        mock_db_session.query.assert_called_once_with(VideoModel)
        
        assert len(result) == 2
        assert result[0].id == video_id1
        assert result[0].filename == "test1.mp4"
        assert result[0].status == VideoStatus.COMPLETED
        assert result[1].id == video_id2
        assert result[1].filename == "test2.mp4"
        assert result[1].status == VideoStatus.PROCESSING
