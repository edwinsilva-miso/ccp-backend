import os
from typing import Optional
import google.cloud.aiplatform as aiplatform
from google.cloud.aiplatform.gapic.schema import predict
from src.domain.ports.video_analyzer_service import VideoAnalyzerService


class VertexAIAnalyzerService(VideoAnalyzerService):
    def __init__(self):
        # Get configuration from environment variables
        self.project_id = os.getenv("GCS_PROJECT_ID")
        self.location = os.getenv("VERTEX_AI_LOCATION")
        self.credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

        # Initialize Vertex AI client
        if self.credentials_path:
            print(f"Using Google credentials from: {self.credentials_path}")
        else:
            print("Using default Google credentials from environment")

        # Initialize the base Vertex AI client
        aiplatform.init(project=self.project_id, location=self.location)

    def analyze_video(self, video_url: str) -> Optional[str]:
        """
        Analyze a video using Vertex AI

        This implementation uses a generative AI model to analyze the video and
        provide insights about product placement opportunities.
        """
        try:
            # Using the Vertex AI Generative AI API for video analysis
            # For Gemini models, we need to use the VertexAI GenerativeModel
            from vertexai.generative_models import GenerativeModel, Part
            import vertexai

            # Initialize Vertex AI with explicit credentials if available
            vertexai.init(project=self.project_id, location=self.location)

            # Load the Gemini Pro Vision model
            multimodal_model = GenerativeModel("gemini-pro-vision")

            # Create a prompt for the model
            prompt = (
                "Analyze this video that shows a place. "
                "Assess how many products could be placed in this location, "
                "and suggest other products that might be relevant for this space. "
                "Provide your analysis as informative text."
            )

            # Create a video part from the GCS URI
            video_part = Part.from_uri(video_url, mime_type="video/mp4")

            # Generate content with the video and prompt
            response = multimodal_model.generate_content([prompt, video_part])

            # Return the generated text
            return response.text

        except Exception as e:
            print(f"Error analyzing video with Vertex AI: {str(e)}")
            return None
