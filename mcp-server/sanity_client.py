"""
Sanity.io client for user profiles and message templates.
"""
import requests
import logging
from typing import Optional, Dict, Any, List

from config import Config

logger = logging.getLogger(__name__)


class SanityClient:
    """Client for interacting with Sanity.io CMS."""

    def __init__(self):
        """Initialize Sanity client."""
        self.project_id = Config.SANITY_PROJECT_ID
        self.dataset = Config.SANITY_DATASET
        self.api_version = Config.SANITY_API_VERSION
        self.token = Config.SANITY_API_TOKEN

        # API endpoints
        self.query_url = f"https://{self.project_id}.api.sanity.io/{self.api_version}/data/query/{self.dataset}"
        self.mutate_url = f"https://{self.project_id}.api.sanity.io/{self.api_version}/data/mutate/{self.dataset}"

        logger.info(f"Initialized Sanity client for project {self.project_id}")

    def _get_headers(self, include_auth: bool = False) -> Dict[str, str]:
        """
        Get request headers.

        Args:
            include_auth: Whether to include authorization token

        Returns:
            Headers dictionary
        """
        headers = {
            "Content-Type": "application/json"
        }

        if include_auth and self.token:
            headers["Authorization"] = f"Bearer {self.token}"

        return headers

    def query(self, groq_query: str, params: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        """
        Execute a GROQ query against Sanity.

        Args:
            groq_query: GROQ query string
            params: Optional query parameters

        Returns:
            Query result or None if error

        Raises:
            requests.RequestException: If request fails
        """
        try:
            response = requests.get(
                self.query_url,
                params={"query": groq_query, **(params or {})},
                headers=self._get_headers(),
                timeout=10
            )
            response.raise_for_status()

            data = response.json()
            return data.get("result")

        except requests.RequestException as e:
            logger.error(f"Sanity query failed: {e}")
            raise

    def get_user_profile(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        Get user profile from Sanity.

        Args:
            user_id: User ID

        Returns:
            User profile or None if not found

        Raises:
            requests.RequestException: If request fails
        """
        query = f"""
            *[_type == "userProfile" && userId == "{user_id}"][0] {{
                _id,
                userId,
                name,
                email,
                phone,
                interests,
                industry,
                role,
                seniority,
                goals,
                bio,
                location,
                linkedinUrl,
                twitterHandle,
                availability
            }}
        """

        result = self.query(query)
        return result

    def update_user_profile(self, user_id: str, data: Dict[str, Any]) -> bool:
        """
        Update user profile in Sanity.

        Args:
            user_id: User ID
            data: Profile data to update

        Returns:
            True if update successful

        Raises:
            requests.RequestException: If request fails
            ValueError: If no API token configured
        """
        if not self.token:
            raise ValueError("Sanity API token required for write operations")

        # First, get existing profile to get _id
        existing_profile = self.get_user_profile(user_id)

        if existing_profile:
            # Update existing profile
            mutation = {
                "mutations": [
                    {
                        "patch": {
                            "id": existing_profile["_id"],
                            "set": data
                        }
                    }
                ]
            }
        else:
            # Create new profile
            mutation = {
                "mutations": [
                    {
                        "create": {
                            "_type": "userProfile",
                            "userId": user_id,
                            **data
                        }
                    }
                ]
            }

        try:
            response = requests.post(
                self.mutate_url,
                json=mutation,
                headers=self._get_headers(include_auth=True),
                timeout=10
            )
            response.raise_for_status()

            logger.info(f"Updated user profile for {user_id}")
            return True

        except requests.RequestException as e:
            logger.error(f"Failed to update user profile: {e}")
            raise

    def get_message_templates(self, template_type: str = "introduction") -> List[Dict[str, Any]]:
        """
        Get message templates from Sanity.

        Args:
            template_type: Type of template to retrieve

        Returns:
            List of message templates

        Raises:
            requests.RequestException: If request fails
        """
        query = f"""
            *[_type == "messageTemplate" && templateType == "{template_type}"] {{
                _id,
                templateType,
                name,
                content,
                variables,
                context
            }}
        """

        result = self.query(query)
        return result if isinstance(result, list) else []

    def create_message_template(self, template_data: Dict[str, Any]) -> bool:
        """
        Create a new message template in Sanity.

        Args:
            template_data: Template data

        Returns:
            True if creation successful

        Raises:
            requests.RequestException: If request fails
            ValueError: If no API token configured
        """
        if not self.token:
            raise ValueError("Sanity API token required for write operations")

        mutation = {
            "mutations": [
                {
                    "create": {
                        "_type": "messageTemplate",
                        **template_data
                    }
                }
            ]
        }

        try:
            response = requests.post(
                self.mutate_url,
                json=mutation,
                headers=self._get_headers(include_auth=True),
                timeout=10
            )
            response.raise_for_status()

            logger.info(f"Created message template: {template_data.get('name')}")
            return True

        except requests.RequestException as e:
            logger.error(f"Failed to create message template: {e}")
            raise


# Global Sanity client instance
sanity = SanityClient()
