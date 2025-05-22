import pytest
from abc import ABC
from typing import BinaryIO

from src.domain.ports.storage_service import StorageService


class TestStorageService:
    def test_is_abstract_base_class(self):
        """Test that StorageService is an abstract base class"""
        assert issubclass(StorageService, ABC)
    
    def test_has_required_abstract_methods(self):
        """Test that StorageService has required abstract methods"""
        # Get abstract methods
        abstract_methods = StorageService.__abstractmethods__
        
        # Check that required methods are abstract
        assert 'upload_file' in abstract_methods
        assert 'get_file_url' in abstract_methods
    
    def test_upload_file_signature(self):
        """Test that upload_file has the correct signature"""
        # Get method signature
        method = StorageService.upload_file
        
        # Check parameter types using __annotations__
        assert method.__annotations__['file_data'] == BinaryIO
        assert method.__annotations__['filename'] == str
        assert method.__annotations__['return'] == str
    
    def test_get_file_url_signature(self):
        """Test that get_file_url has the correct signature"""
        # Get method signature
        method = StorageService.get_file_url
        
        # Check parameter types using __annotations__
        assert method.__annotations__['filename'] == str
        assert method.__annotations__['return'] == str
