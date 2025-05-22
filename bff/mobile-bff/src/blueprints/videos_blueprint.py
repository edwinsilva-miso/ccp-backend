import logging
from flask import Blueprint, request

from ..adapters.videos_adapter import VideosAdapter
from ..utils.commons import validate_token

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

videos_blueprint = Blueprint('videos', __name__, url_prefix='/bff/v1/mobile/videos')


@videos_blueprint.route('/upload', methods=['POST'])
@validate_token
def upload_video(jwt):
    """Upload a video file."""
    logger.debug("received request to upload a video")

    if 'video' not in request.files:
        return {"error": "No video file in request"}, 400

    video_file = request.files['video']

    if not video_file.filename:
        return {"error": "Empty filename"}, 400

    adapter = VideosAdapter()
    return adapter.upload_video(jwt, video_file)


@videos_blueprint.route('/<video_id>/status', methods=['GET'])
@validate_token
def get_video_status(video_id, jwt):
    """Get the status of a video."""
    logger.debug(f"received request to get status for video with id: {video_id}")

    adapter = VideosAdapter()
    return adapter.get_video_status(jwt, video_id)


@videos_blueprint.route('', methods=['GET'])
@validate_token
def list_videos(jwt):
    """List all videos."""
    logger.debug("received request to list all videos")

    adapter = VideosAdapter()
    return adapter.list_videos(jwt)