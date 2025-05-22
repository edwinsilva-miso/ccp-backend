import pytest
from abc import ABC
from typing import Optional, List

from src.domain.ports.video_repository import VideoRepository
from src.domain.models.video import Video


class TestVideoRepository:
    def test_is_abstract_base_class(self):
        """Test that VideoRepository is an abstract base class"""
        assert issubclass(VideoRepository, ABC)
    
    def test_has_required_abstract_methods(self):
        """Test that VideoRepository has required abstract methods"""
        # Get abstract methods
        abstract_methods = VideoRepository.__abstractmethods__
        
        # Check that required methods are abstract
        assert 'save' in abstract_methods
        assert 'update' in abstract_methods
        assert 'get_by_id' in abstract_methods
        assert 'list_all' in abstract_methods
    
    def test_save_signature(self):
        """Test that save has the correct signature"""
        # Get method signature
        method = VideoRepository.save
        
        # Check parameter types using __annotations__
        assert method.__annotations__['video'] == Video
        assert method.__annotations__['return'] == Video
    
    def test_update_signature(self):
        """Test that update has the correct signature"""
        # Get method signature
        method = VideoRepository.update
        
        # Check parameter types using __annotations__
        assert method.__annotations__['video'] == Video
        assert method.__annotations__['return'] == Video
    
    def test_get_by_id_signature(self):
        """Test that get_by_id has the correct signature"""
        # Get method signature
        method = VideoRepository.get_by_id
        
        # Check parameter types using __annotations__
        assert method.__annotations__['video_id'] == str
        assert method.__annotations__['return'] == Optional[Video]
    
    def test_list_all_signature(self):
        """Test that list_all has the correct signature"""
        # Get method signature
        method = VideoRepository.list_all
        
        # Check parameter types using __annotations__
        assert method.__annotations__['return'] == List[Video]
