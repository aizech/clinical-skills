"""HTTP client with retry logic, rate limiting, and timeout handling."""

import logging
import time
from typing import Optional

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


logger = logging.getLogger(__name__)


class APIClient:
    """HTTP client with retry logic and rate limiting."""

    def __init__(
        self,
        base_url: str,
        timeout: int = 30,
        max_retries: int = 3,
        backoff_factor: float = 0.5,
        status_forcelist: Optional[list[int]] = None,
    ):
        """Initialize API client.

        Args:
            base_url: Base URL for API requests
            timeout: Request timeout in seconds
            max_retries: Maximum number of retry attempts
            backoff_factor: Backoff factor for exponential backoff
            status_forcelist: HTTP status codes to retry on
        """
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = self._create_session(max_retries, backoff_factor, status_forcelist)

    def _create_session(
        self,
        max_retries: int,
        backoff_factor: float,
        status_forcelist: Optional[list[int]],
    ) -> requests.Session:
        """Create a requests session with retry strategy.

        Args:
            max_retries: Maximum retry attempts
            backoff_factor: Exponential backoff factor
            status_forcelist: Status codes to retry

        Returns:
            Configured requests.Session
        """
        if status_forcelist is None:
            status_forcelist = [429, 500, 502, 503, 504]

        retry_strategy = Retry(
            total=max_retries,
            backoff_factor=backoff_factor,
            status_forcelist=status_forcelist,
            allowed_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
        )

        adapter = HTTPAdapter(max_retries=retry_strategy)
        session = requests.Session()
        session.mount("http://", adapter)
        session.mount("https://", adapter)

        return session

    def get(
        self,
        endpoint: str,
        params: Optional[dict] = None,
        headers: Optional[dict] = None,
    ) -> requests.Response:
        """Perform GET request with retry logic.

        Args:
            endpoint: API endpoint path
            params: Query parameters
            headers: Request headers

        Returns:
            requests.Response object

        Raises:
            requests.RequestException: On request failure
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        logger.debug(f"GET {url} with params: {params}")

        try:
            response = self.session.get(
                url,
                params=params,
                headers=headers,
                timeout=self.timeout,
            )
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            logger.error(f"GET request failed: {e}")
            raise

    def post(
        self,
        endpoint: str,
        data: Optional[dict] = None,
        json: Optional[dict] = None,
        headers: Optional[dict] = None,
    ) -> requests.Response:
        """Perform POST request with retry logic.

        Args:
            endpoint: API endpoint path
            data: Form data
            json: JSON data
            headers: Request headers

        Returns:
            requests.Response object

        Raises:
            requests.RequestException: On request failure
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        logger.debug(f"POST {url}")

        try:
            response = self.session.post(
                url,
                data=data,
                json=json,
                headers=headers,
                timeout=self.timeout,
            )
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            logger.error(f"POST request failed: {e}")
            raise

    def close(self) -> None:
        """Close the session."""
        self.session.close()


class BearerTokenAuth:
    """Bearer token authentication helper."""

    def __init__(self, token: str):
        """Initialize with bearer token.

        Args:
            token: Bearer token string
        """
        self.token = token

    def get_headers(self) -> dict:
        """Get headers with Authorization header.

        Returns:
            Dictionary with Authorization header
        """
        return {"Authorization": f"Bearer {self.token}"}
