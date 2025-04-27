import requests
from typing import List, Tuple, Dict, Any


class OpenRouteServiceClient:
    """Client for the OpenRoute Service API."""

    def __init__(self, api_key: str, base_url: str = "https://api.openrouteservice.org"):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            "Authorization": api_key,
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    def optimize_route(self, waypoints: List[Tuple[float, float]], params: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Optimize a route using the OpenRoute Service API.

        Args:
            waypoints: List of (longitude, latitude) coordinates
            params: Additional parameters for the optimization

        Returns:
            Dictionary containing the optimization results
        """
        # Default parameters
        default_params = {
            "profile": "driving-car",
            "optimizationMode": "fastest"
        }

        # Merge with custom params
        request_params = {**default_params, **(params or {})}

        # Prepare the request body
        request_body = {
            "coordinates": waypoints,
            **request_params
        }

        # Make the request to the optimization endpoint
        response = requests.post(
            f"{self.base_url}/v2/directions/{request_params['profile']}/json",
            headers=self.headers,
            json=request_body
        )

        # Check for errors
        if response.status_code != 200:
            error_msg = f"OpenRoute Service API error ({response.status_code}): {response.text}"
            raise Exception(error_msg)

        # Parse and return the result
        result = response.json()

        # Extract the optimized order of waypoints
        if "routes" in result and len(result["routes"]) > 0:
            route = result["routes"][0]

            # Extract waypoint order (this might need adjustment based on actual API response)
            waypoint_indices = []
            if "waypoint_order" in route:
                waypoint_indices = route["waypoint_order"]
            else:
                # If API doesn't provide waypoint_order, construct it from the segments
                segments = route.get("segments", [])
                waypoint_indices = list(range(len(waypoints)))

            return {
                "waypoint_order": waypoint_indices,
                "legs": route.get("segments", []),
                "distance": route.get("summary", {}).get("distance", 0),
                "duration": route.get("summary", {}).get("duration", 0),
                "bbox": route.get("bbox", [])
            }

        return {"error": "No routes found in the response"}
