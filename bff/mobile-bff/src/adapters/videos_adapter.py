import logging
import os
import requests

VIDEOS_API_URL = os.environ.get('MARKET_INTELLIGENCE_API_URL', 'http://localhost:5000')

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger(__name__)


class VideosAdapter:
    @staticmethod
    def upload_video(jwt, video_file):
        """
        Upload a video file to the market-intelligence-api

        Args:
            jwt: JWT token for authentication
            video_file: The video file to upload

        Returns:
            Response from the API and status code
        """
        logger.debug(f"uploading video file: {video_file.filename}")

        files = {'video': (video_file.filename, video_file, video_file.content_type)}

        response = requests.post(
            url=f"{VIDEOS_API_URL}/api/videos/upload",
            headers={'Authorization': f'Bearer {jwt}'},
            files=files
        )

        logger.debug(f"response received from videos api: {response.json()}")

        return response.json(), response.status_code

    @staticmethod
    def get_video_status(jwt, video_id):
        """
        Get the status of a video

        Args:
            jwt: JWT token for authentication
            video_id: ID of the video

        Returns:
            Response from the API and status code
        """
        logger.debug(f"getting status for video with ID: {video_id}")

        response = requests.get(
            url=f"{VIDEOS_API_URL}/api/videos/{video_id}/status",
            headers={'Authorization': f'Bearer {jwt}'}
        )

        logger.debug(f"response received from videos api: {response.json()}")

        return response.json(), response.status_code

    @staticmethod
    def list_videos(jwt):
        """
        List all videos

        Args:
            jwt: JWT token for authentication

        Returns:
            Response from the API and status code
        """
        logger.debug("listing all videos")

        response = requests.get(
            url=f"{VIDEOS_API_URL}/api/videos/",
            headers={'Authorization': f'Bearer {jwt}'}
        )

        logger.debug(f"response received from videos api: {response.json()}")

        return response.json(), response.status_code