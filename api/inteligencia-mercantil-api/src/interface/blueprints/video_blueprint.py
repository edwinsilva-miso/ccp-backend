from flask import Blueprint, request, jsonify
from src.application.use_cases.video_processor import VideoProcessor
from src.infrastructure.adapters.sqlalchemy_video_repository import SQLAlchemyVideoRepository
from src.infrastructure.adapters.gcs_storage_service import GCSStorageService
from src.infrastructure.adapters.vertex_ai_analyzer_service import VertexAIAnalyzerService

# Create blueprint
video_blueprint = Blueprint("video", __name__)

# Initialize dependencies
video_repository = SQLAlchemyVideoRepository()
storage_service = GCSStorageService()
analyzer_service = VertexAIAnalyzerService()
video_processor = VideoProcessor(video_repository, storage_service, analyzer_service)


@video_blueprint.route("/upload", methods=["POST"])
def upload_video():
    """
    Upload a video file
    
    Returns:
        A JSON response with the video ID and status
    """
    if "video" not in request.files:
        return jsonify({"error": "No video file in request"}), 400
    
    video_file = request.files["video"]
    
    if not video_file.filename:
        return jsonify({"error": "Empty filename"}), 400
    
    # Process the uploaded video
    video = video_processor.upload_video(video_file, video_file.filename)
    
    return jsonify({
        "id": video.id,
        "filename": video.filename,
        "status": video.status.value,
        "message": "Video uploaded successfully and queued for processing"
    }), 200


@video_blueprint.route("/<video_id>/status", methods=["GET"])
def get_video_status(video_id):
    """
    Get the status of a video
    
    Args:
        video_id: The ID of the video
        
    Returns:
        A JSON response with the video status and analysis result if available
    """
    video = video_processor.get_video_status(video_id)
    
    if not video:
        return jsonify({"error": "Video not found"}), 404
    
    response = {
        "id": video.id,
        "filename": video.filename,
        "status": video.status.value,
        "created_at": video.created_at.isoformat(),
        "updated_at": video.updated_at.isoformat()
    }
    
    if video.analysis_result:
        response["analysis_result"] = video.analysis_result
    
    return jsonify(response), 200


@video_blueprint.route("/", methods=["GET"])
def list_videos():
    """
    List all videos
    
    Returns:
        A JSON response with a list of videos
    """
    videos = video_repository.list_all()
    
    return jsonify([
        {
            "id": video.id,
            "filename": video.filename,
            "status": video.status.value,
            "created_at": video.created_at.isoformat(),
            "updated_at": video.updated_at.isoformat()
        }
        for video in videos
    ]), 200
