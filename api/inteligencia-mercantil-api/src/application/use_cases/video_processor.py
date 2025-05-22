from typing import BinaryIO, Optional
from datetime import datetime
import threading
from flask import current_app, copy_current_request_context
from src.domain.models.video import Video, VideoStatus
from src.domain.ports.video_repository import VideoRepository
from src.domain.ports.storage_service import StorageService
from src.domain.ports.video_analyzer_service import VideoAnalyzerService


class VideoProcessor:
    def __init__(
        self,
        video_repository: VideoRepository,
        storage_service: StorageService,
        analyzer_service: VideoAnalyzerService,
    ):
        self.video_repository = video_repository
        self.storage_service = storage_service
        self.analyzer_service = analyzer_service
    
    def upload_video(self, file_data: BinaryIO, filename: str) -> Video:
        """
        Upload a video file to storage and save its metadata to the repository
        
        Args:
            file_data: The video file data
            filename: The name of the file
            
        Returns:
            The saved video entity
        """
        # Upload file to storage
        gcs_url = self.storage_service.upload_file(file_data, filename)
        
        # Create and save video entity
        video = Video(
            filename=filename,
            gcs_url=gcs_url,
            status=VideoStatus.UPLOADED,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        saved_video = self.video_repository.save(video)
        
        # Start asynchronous processing of the video in a separate thread
        self._process_video_async(saved_video.id)
        
        return saved_video
    
    def process_video(self, video_id: str) -> None:
        """
        Process a video with Vertex AI
        
        Args:
            video_id: The ID of the video to process
        """
        # Get video from repository
        video = self.video_repository.get_by_id(video_id)
        
        if not video:
            return
        
        # Update status to processing
        video.status = VideoStatus.PROCESSING
        video.updated_at = datetime.utcnow()
        self.video_repository.update(video)
        
        # Analyze video with Vertex AI
        try:
            analysis_result = self.analyzer_service.analyze_video(video.gcs_url)
            
            # Update video with analysis result
            video.analysis_result = analysis_result
            video.status = VideoStatus.COMPLETED if analysis_result else VideoStatus.FAILED
        except Exception as e:
            video.status = VideoStatus.FAILED
            video.analysis_result = f"Error analyzing video: {str(e)}"
        
        video.updated_at = datetime.utcnow()
        self.video_repository.update(video)
    
    def get_video_status(self, video_id: str) -> Optional[Video]:
        """
        Get the status of a video
        
        Args:
            video_id: The ID of the video
            
        Returns:
            The video entity, or None if not found
        """
        return self.video_repository.get_by_id(video_id)
    
    def _process_video_async(self, video_id: str) -> None:
        """
        Procesa un video de forma asíncrona en un hilo separado mientras
        mantiene el contexto de la aplicación Flask.
        
        Args:
            video_id: El ID del video a procesar
        """
        # Capturar el contexto actual de la aplicación si existe
        try:
            app = current_app._get_current_object()
            
            # Envolver el procesamiento en el contexto de la aplicación
            @copy_current_request_context
            def process_with_context():
                with app.app_context():
                    self.process_video(video_id)
            
            # Iniciar un nuevo hilo para el procesamiento
            thread = threading.Thread(target=process_with_context)
            thread.daemon = True  # El hilo terminará cuando el programa principal termine
            thread.start()
            
        except RuntimeError:
            # Si no estamos en un contexto de Flask, ejecutamos directamente
            # (esto ocurriría si se llama desde scripts u otros contextos)
            thread = threading.Thread(target=self.process_video, args=(video_id,))
            thread.daemon = True
            thread.start()
