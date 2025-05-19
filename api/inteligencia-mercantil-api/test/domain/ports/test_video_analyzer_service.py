import pytest
from abc import ABC
from typing import Optional

from src.domain.ports.video_analyzer_service import VideoAnalyzerService


class TestVideoAnalyzerService:
    def test_is_abstract_base_class(self):
        """Test that VideoAnalyzerService is an abstract base class"""
        assert issubclass(VideoAnalyzerService, ABC)
    
    def test_has_required_abstract_methods(self):
        """Test that VideoAnalyzerService has required abstract methods"""
        # Get abstract methods
        abstract_methods = VideoAnalyzerService.__abstractmethods__
        
        # Check that required methods are abstract
        assert 'analyze_video' in abstract_methods
    
    def test_analyze_video_signature(self):
        """Test that analyze_video has the correct signature"""
        # Get method signature
        method = VideoAnalyzerService.analyze_video
        
        # Check parameter types using __annotations__
        assert method.__annotations__['video_url'] == str
        assert method.__annotations__['return'] == Optional[str]
