from typing import Optional
from src.domain.ports.video_analyzer_service import VideoAnalyzerService
from src.domain.ports.video_analyzer_service import VideoAnalyzerService


class MockAnalyzerService(VideoAnalyzerService):
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

class MockAnalyzerService(VideoAnalyzerService):
    """
    A mock implementation of the VideoAnalyzerService for testing purposes.
    This avoids using Vertex AI in tests.
    """
    
    def __init__(self, return_value=None, raise_exception=False, exception_message=None):
        """
        Initialize the mock analyzer with configurable behavior.
        
        Args:
            return_value: The value to return from analyze_video
            raise_exception: Whether to raise an exception
            exception_message: The message for the exception if raised
        """
        self.return_value = return_value or "Mock analysis result"
        self.raise_exception = raise_exception
        self.exception_message = exception_message or "Mock analysis error"
        self.called_with = None
        self.call_count = 0
    
    def analyze_video(self, video_url: str) -> Optional[str]:
        """
        Mock implementation that either returns a predefined result or raises an exception.
        
        Args:
            video_url: The URL of the video to analyze
            
        Returns:
            A predefined analysis result or None
            
        Raises:
            Exception: If configured to raise an exception
        """
        self.called_with = video_url
        self.call_count += 1
        
        if self.raise_exception:
            raise Exception(self.exception_message)
        
        return self.return_value
