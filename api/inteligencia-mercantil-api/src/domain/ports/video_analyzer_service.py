from abc import ABC, abstractmethod
from typing import Optional


class VideoAnalyzerService(ABC):
    @abstractmethod
    def analyze_video(self, video_url: str) -> Optional[str]:
        """
        Analyze a video using AI
        
        Args:
            video_url: The URL of the video to analyze
            
        Returns:
            The analysis result as text, or None if analysis failed
        """
        pass
