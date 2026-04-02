"""Low-level synchronous REST client for the Polygon.io API."""
from __future__ import annotations

import sys
from typing import Any

import httpx


class PolygonAPIError(Exception):
    """Raised when Polygon API returns an error response."""

    def __init__(self, status_code: int, message: str) -> None:
        self.status_code = status_code
        super().__init__(f"Polygon API {status_code}: {message}")


class PolygonClient:
    """Synchronous REST client for Polygon.io API."""

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.polygon.io",
        timeout: float = 30.0,
    ) -> None:
        self.api_key = api_key
        self.base_url = base_url
        self.timeout = timeout
        self._session = httpx.Client(timeout=timeout)

    def _build_url(self, path: str) -> str:
        """Return the full URL by joining base_url with path."""
        return self.base_url + path

    def _default_params(self) -> dict[str, Any]:
        """Return query parameters that are included in every request."""
        return {"apiKey": self.api_key}

    def get(self, path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        """Perform a GET request and return the parsed JSON body.

        Args:
            path: API path (e.g. "/v2/aggs/ticker/AAPL/range/1/day/...").
            params: Optional extra query parameters to merge with defaults.

        Returns:
            Parsed JSON response as a dict.

        Raises:
            PolygonAPIError: If the response status code is not 2xx.
        """
        print(f"[polygon] GET {path}", file=sys.stderr)

        merged_params: dict[str, Any] = {**self._default_params()}
        if params:
            merged_params.update(params)

        url = self._build_url(path)
        response = self._session.get(url, params=merged_params)

        if not (200 <= response.status_code < 300):
            raise PolygonAPIError(response.status_code, response.text)

        return response.json()

    def close(self) -> None:
        """Close the underlying httpx session."""
        self._session.close()
