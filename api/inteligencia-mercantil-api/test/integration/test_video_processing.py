import pytest
import os
import json
from unittest.mock import patch, MagicMock
from io import BytesIO

from src.main import create_app
from src.domain.models.video import VideoStatus


# Create mock classes here instead of importing from src.infrastructure.mocks
class MockStorageService:
    def __init__(self):
        self.uploaded_files = {}
    
    def upload_file(self, file_data, filename):
        self.uploaded_files[filename] = file_data.read()
        return f"gs://test-bucket/{filename}"
    
    def get_file_url(self, filename):
        return f"gs://test-bucket/{filename}"


class MockAnalyzerService:
    def __init__(self):
        self.analyzed_videos = {}
        self.return_value = "Mock analysis result"
        self.raise_exception = False
        self.exception_message = "Mock analyzer error"
    
    def analyze_video(self, video_url):
        if self.raise_exception:
            raise Exception(self.exception_message)
        
        self.analyzed_videos[video_url] = True
        return self.return_value


class MockVideoRepository:
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


@pytest.fixture
def mock_google_services():
    # Mock Google Cloud metadata server
    with patch('requests.get') as mock_get:
        mock_get.return_value.text = "fake-service-account@test.iam.gserviceaccount.com"
        # Mock Google credentials
        with patch('google.auth.default') as mock_default:
            mock_default.return_value = (MagicMock(), "test-project")
            yield


@pytest.fixture
def mock_services():
    # Create mock services
    mock_repo = MockVideoRepository()
    mock_storage = MockStorageService()
    mock_analyzer = MockAnalyzerService()
    
    # Import VideoProcessor here to avoid circular imports
    from src.application.use_cases.video_processor import VideoProcessor
    
    # Create video processor with mocks
    processor = VideoProcessor(mock_repo, mock_storage, mock_analyzer)
    
    return mock_repo, mock_storage, mock_analyzer, processor


@pytest.fixture
def app():
    """Create a Flask app for testing"""
    # Set required environment variables
    with patch.dict('os.environ', {
        'DB_USER': 'test_user',
        'DB_PASSWORD': 'test_password',
        'DB_HOST': 'localhost',
        'DB_PORT': '5432',
        'DB_NAME': 'test_db',
        'GCS_BUCKET_NAME': 'test-bucket'
    }):
        # Mock the Google Cloud metadata server request
        with patch('requests.get') as mock_get:
            mock_get.return_value.text = "fake-service-account@test.iam.gserviceaccount.com"
            # Mock Google credentials
            with patch('google.auth.default') as mock_default:
                mock_default.return_value = (MagicMock(), "test-project")
                # Mock database connection
                with patch('src.infrastructure.database.models.db.create_all'):
                    app = create_app()
                    app.config['TESTING'] = True
                    yield app


@pytest.fixture
def app_client(app, mock_services):
    """Create a test client with mocked services"""
    # Get mock services
    mock_repo, mock_storage, mock_analyzer, processor = mock_services
    
    # Replace services in blueprint with mocks
    with patch('src.interface.blueprints.video_blueprint.video_repository', mock_repo), \
         patch('src.interface.blueprints.video_blueprint.storage_service', mock_storage), \
         patch('src.interface.blueprints.video_blueprint.analyzer_service', mock_analyzer), \
         patch('src.interface.blueprints.video_blueprint.video_processor', processor), \
         patch('google.cloud.storage.Client'):
        
        with app.test_client() as client:
            with app.app_context():
                yield client, mock_repo, mock_storage, mock_analyzer, processor


class TestVideoProcessingIntegration:
    @pytest.mark.skip("Integration test skipped for CI environment")
    def test_end_to_end_flow(self, app_client):
        """Test the complete flow from upload to processing"""
        # Arrange
        client, mock_repo, mock_storage, mock_analyzer, processor = app_client
        
        # Create a test video file
        test_video = BytesIO(b'test video content')
        test_filename = 'integration_test.mp4'
        
        # Step 1: Upload the video
        response = client.post(
            '/api/videos/upload',
            data={'video': (test_video, test_filename)},
            content_type='multipart/form-data'
        )
        
        # Check upload was successful
        assert response.status_code == 200
        response_data = json.loads(response.data)
        video_id = response_data['id']
        
        # Step 2: Process the uploaded video (normally happens in background)
        # Since we're testing, we'll force process the video synchronously
        processor.process_video(video_id)
        
        # Step 3: Check video status
        status_response = client.get(f'/api/videos/{video_id}/status')
        
        # Check status response
        assert status_response.status_code == 200
        status_data = json.loads(status_response.data)
        assert status_data['status'] == VideoStatus.COMPLETED.value
        assert 'analysis_result' in status_data
        assert status_data['analysis_result'] == mock_analyzer.return_value
        
        # Step 4: Check list of videos endpoint
        list_response = client.get('/api/videos/')
        
        # Check list response
        assert list_response.status_code == 200
        list_data = json.loads(list_response.data)
        assert len(list_data) == 1
        assert list_data[0]['id'] == video_id
        assert list_data[0]['filename'] == test_filename
        assert list_data[0]['status'] == VideoStatus.COMPLETED.value
    
    @pytest.mark.skip("Integration test skipped for CI environment")
    def test_error_handling_in_processing(self, app_client):
        """Test error handling during video processing"""
        # Arrange
        client, mock_repo, mock_storage, mock_analyzer, processor = app_client
        
        # Configure analyzer to fail
        mock_analyzer.raise_exception = True
        mock_analyzer.exception_message = "Test processing error"
        
        # Create a test video file
        test_video = BytesIO(b'test error content')
        test_filename = 'error_test.mp4'
        
        # Step 1: Upload the video
        response = client.post(
            '/api/videos/upload',
            data={'video': (test_video, test_filename)},
            content_type='multipart/form-data'
        )
        
        # Check upload was successful
        assert response.status_code == 200
        response_data = json.loads(response.data)
        video_id = response_data['id']
        
        # Step 2: Process the video (should fail)
        processor.process_video(video_id)
        
        # Step 3: Check video status
        status_response = client.get(f'/api/videos/{video_id}/status')
        
        # Check status shows failure
        assert status_response.status_code == 200
        status_data = json.loads(status_response.data)
        assert status_data['status'] == VideoStatus.FAILED.value
        assert 'analysis_result' in status_data
        assert "Error analyzing video: Test processing error" in status_data['analysis_result']
    
    @pytest.mark.skip("Integration test skipped for CI environment")
    def test_non_existent_video_status(self, app_client):
        """Test getting status of non-existent video"""
        # Arrange
        client, *_ = app_client
        non_existent_id = "00000000-0000-0000-0000-000000000000"
        
        # Act
        response = client.get(f'/api/videos/{non_existent_id}/status')
        
        # Assert
        assert response.status_code == 404
        response_data = json.loads(response.data)
        assert 'error' in response_data
        assert 'Video not found' in response_data['error']
