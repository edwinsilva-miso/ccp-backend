import pytest
from unittest.mock import patch, MagicMock
import os

from src.infrastructure.adapters.vertex_ai_analyzer_service import VertexAIAnalyzerService


class TestVertexAIAnalyzerService:
    @pytest.fixture
    def mock_vertex_ai(self):
        with patch('google.cloud.aiplatform.init') as mock_init:
            yield mock_init
    
    @pytest.fixture
    def service(self, mock_vertex_ai):
        # Set environment variables for the test
        os.environ["GCS_PROJECT_ID"] = "test-project"
        os.environ["VERTEX_AI_LOCATION"] = "us-central1"
        
        # Create service with mocked dependencies
        return VertexAIAnalyzerService()
    
    def test_init(self, mock_vertex_ai):
        """Test that the service initializes correctly"""
        # Arrange
        os.environ["GCS_PROJECT_ID"] = "test-project"
        os.environ["VERTEX_AI_LOCATION"] = "us-central1"
        
        # Act
        service = VertexAIAnalyzerService()
        
        # Assert
        mock_vertex_ai.assert_called_once_with(
            project="test-project", 
            location="us-central1"
        )
        assert service.project_id == "test-project"
        assert service.location == "us-central1"
    
    def test_analyze_video_success(self, service):
        """Test that analyze_video processes a video successfully"""
        # Arrange
        video_url = "gs://test-bucket/test.mp4"
        
        # Mock the GenerativeModel
        mock_response = MagicMock()
        mock_response.text = "Test analysis result"
        
        mock_model = MagicMock()
        mock_model.generate_content.return_value = mock_response
        
        mock_part = MagicMock()
        
        # Act
        with patch('vertexai.init') as mock_init, \
             patch('vertexai.generative_models.GenerativeModel', return_value=mock_model) as mock_gen_model, \
             patch('vertexai.generative_models.Part.from_uri', return_value=mock_part) as mock_part_from_uri:
            
            result = service.analyze_video(video_url)
        
        # Assert
        mock_init.assert_called_once_with(project="test-project", location="us-central1")
        mock_gen_model.assert_called_once_with("gemini-2.5-pro-preview-05-06")
        mock_part_from_uri.assert_called_once_with(video_url, mime_type="video/mp4")
        mock_model.generate_content.assert_called_once()
        assert result == "Test analysis result"
    
    def test_analyze_video_error(self, service):
        """Test that analyze_video handles errors properly"""
        # Arrange
        video_url = "gs://test-bucket/test.mp4"
        
        # Act
        with patch('vertexai.init') as mock_init, \
             patch('vertexai.generative_models.GenerativeModel') as mock_gen_model:
            
            mock_gen_model.side_effect = Exception("Analysis failed")
            result = service.analyze_video(video_url)
        
        # Assert
        assert result is None
