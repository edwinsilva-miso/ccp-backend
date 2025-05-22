import uuid
from src.domain.models.video import Video, VideoStatus
from src.domain.ports.video_repository import VideoRepository
from src.infrastructure.database.models import db, VideoModel


class SQLAlchemyVideoRepository(VideoRepository):
    def save(self, video: Video) -> Video:
        if not video.id:
            video.id = str(uuid.uuid4())
        
        video_model = VideoModel(
            id=video.id,
            filename=video.filename,
            gcs_url=video.gcs_url,
            status=video.status.value,
            analysis_result=video.analysis_result,
            created_at=video.created_at,
            updated_at=video.updated_at
        )
        
        db.session.add(video_model)
        db.session.commit()
        
        return video
    
    def get_by_id(self, video_id: str) -> Video:
        video_model = VideoModel.query.filter_by(id=video_id).first()
        
        if not video_model:
            return None
            
        return Video(
            id=video_model.id,
            filename=video_model.filename,
            gcs_url=video_model.gcs_url,
            status=VideoStatus(video_model.status),
            analysis_result=video_model.analysis_result,
            created_at=video_model.created_at,
            updated_at=video_model.updated_at
        )
    
    def update(self, video: Video) -> Video:
        video_model = VideoModel.query.filter_by(id=video.id).first()
        
        if not video_model:
            return None
            
        video_model.filename = video.filename
        video_model.gcs_url = video.gcs_url
        video_model.status = video.status.value
        video_model.analysis_result = video.analysis_result
        video_model.updated_at = video.updated_at
        
        db.session.commit()
        
        return video
    
    def list_all(self):
        video_models = VideoModel.query.all()
        
        return [
            Video(
                id=model.id,
                filename=model.filename,
                gcs_url=model.gcs_url,
                status=VideoStatus(model.status),
                analysis_result=model.analysis_result,
                created_at=model.created_at,
                updated_at=model.updated_at
            )
            for model in video_models
        ]
