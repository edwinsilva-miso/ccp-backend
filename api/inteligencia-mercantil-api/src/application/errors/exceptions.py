class VideoProcessorError(Exception):
    """Base error class for video processor"""
    pass


class VideoNotFoundError(VideoProcessorError):
    """Error when a video is not found"""
    pass


class StorageServiceError(VideoProcessorError):
    """Error when interacting with the storage service"""
    pass


class VideoAnalyzerError(VideoProcessorError):
    """Error when analyzing a video"""
    pass
