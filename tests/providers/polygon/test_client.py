"""Tests for PolygonClient low-level HTTP client."""
from __future__ import annotations

from unittest.mock import MagicMock, patch

import httpx
import pytest

from finance_mcp.providers.polygon.client import PolygonAPIError, PolygonClient


class TestPolygonAPIError:
    """Tests for PolygonAPIError exception class."""

    def test_stores_status_code(self) -> None:
        err = PolygonAPIError(403, "Forbidden")
        assert err.status_code == 403

    def test_message_includes_status_and_text(self) -> None:
        err = PolygonAPIError(403, "Forbidden")
        assert "403" in str(err)
        assert "Forbidden" in str(err)

    def test_is_exception(self) -> None:
        err = PolygonAPIError(500, "Internal Server Error")
        assert isinstance(err, Exception)


class TestPolygonClientInit:
    """Tests for PolygonClient.__init__."""

    def test_init_stores_api_key(self) -> None:
        client = PolygonClient(api_key="test-key-123")
        assert client.api_key == "test-key-123"
        client.close()

    def test_base_url_default(self) -> None:
        client = PolygonClient(api_key="test-key")
        assert client.base_url == "https://api.polygon.io"
        client.close()

    def test_base_url_custom(self) -> None:
        client = PolygonClient(api_key="test-key", base_url="https://custom.example.com")
        assert client.base_url == "https://custom.example.com"
        client.close()

    def test_timeout_default(self) -> None:
        client = PolygonClient(api_key="test-key")
        assert client.timeout == 30.0
        client.close()

    def test_creates_httpx_session(self) -> None:
        client = PolygonClient(api_key="test-key")
        assert hasattr(client, "_session")
        assert isinstance(client._session, httpx.Client)
        client.close()


class TestPolygonClientBuildUrl:
    """Tests for PolygonClient._build_url."""

    def test_build_url(self) -> None:
        client = PolygonClient(api_key="test-key")
        url = client._build_url("/v2/aggs/ticker/AAPL/range/1/day/2023-01-01/2023-01-31")
        assert url == "https://api.polygon.io/v2/aggs/ticker/AAPL/range/1/day/2023-01-01/2023-01-31"
        client.close()

    def test_build_url_custom_base(self) -> None:
        client = PolygonClient(api_key="test-key", base_url="https://staging.polygon.io")
        url = client._build_url("/v3/reference/tickers")
        assert url == "https://staging.polygon.io/v3/reference/tickers"
        client.close()


class TestPolygonClientDefaultParams:
    """Tests for PolygonClient._default_params."""

    def test_default_params_include_apikey(self) -> None:
        client = PolygonClient(api_key="my-api-key")
        params = client._default_params()
        assert params == {"apiKey": "my-api-key"}
        client.close()


class TestPolygonClientGet:
    """Tests for PolygonClient.get."""

    def test_get_sync_success(self) -> None:
        """GET request returns parsed JSON on 2xx response."""
        mock_response = MagicMock(spec=httpx.Response)
        mock_response.status_code = 200
        mock_response.json.return_value = {"status": "OK", "results": [{"c": 150.0}]}

        client = PolygonClient(api_key="test-key")
        with patch.object(client._session, "get", return_value=mock_response) as mock_get:
            result = client.get("/v2/aggs/ticker/AAPL/range/1/day/2023-01-01/2023-01-31")

        assert result == {"status": "OK", "results": [{"c": 150.0}]}
        mock_get.assert_called_once()
        client.close()

    def test_get_merges_default_params(self) -> None:
        """GET merges apiKey into any extra params passed."""
        mock_response = MagicMock(spec=httpx.Response)
        mock_response.status_code = 200
        mock_response.json.return_value = {"status": "OK"}

        client = PolygonClient(api_key="test-key")
        with patch.object(client._session, "get", return_value=mock_response) as mock_get:
            client.get("/v3/reference/tickers", params={"ticker": "AAPL"})

        _call_kwargs = mock_get.call_args
        sent_params = _call_kwargs.kwargs.get("params") or _call_kwargs.args[1] if len(_call_kwargs.args) > 1 else _call_kwargs.kwargs.get("params")
        # Params should contain both apiKey and ticker
        assert sent_params is not None
        assert "apiKey" in sent_params
        assert sent_params["apiKey"] == "test-key"
        client.close()

    def test_get_sync_403_raises(self) -> None:
        """GET raises PolygonAPIError on 403 response."""
        mock_response = MagicMock(spec=httpx.Response)
        mock_response.status_code = 403
        mock_response.text = "Forbidden"

        client = PolygonClient(api_key="bad-key")
        with patch.object(client._session, "get", return_value=mock_response):
            with pytest.raises(PolygonAPIError) as exc_info:
                client.get("/v2/aggs/ticker/AAPL/range/1/day/2023-01-01/2023-01-31")

        assert exc_info.value.status_code == 403
        client.close()

    def test_get_sync_500_raises(self) -> None:
        """GET raises PolygonAPIError on 5xx response."""
        mock_response = MagicMock(spec=httpx.Response)
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"

        client = PolygonClient(api_key="test-key")
        with patch.object(client._session, "get", return_value=mock_response):
            with pytest.raises(PolygonAPIError) as exc_info:
                client.get("/v2/aggs/ticker/AAPL/range/1/day/2023-01-01/2023-01-31")

        assert exc_info.value.status_code == 500
        client.close()

    def test_get_logs_to_stderr(self, capsys: pytest.CaptureFixture) -> None:
        """GET logs path to stderr."""
        mock_response = MagicMock(spec=httpx.Response)
        mock_response.status_code = 200
        mock_response.json.return_value = {}

        client = PolygonClient(api_key="test-key")
        with patch.object(client._session, "get", return_value=mock_response):
            client.get("/v3/reference/tickers")

        captured = capsys.readouterr()
        assert "[polygon] GET /v3/reference/tickers" in captured.err
        client.close()


class TestPolygonClientClose:
    """Tests for PolygonClient.close."""

    def test_close_closes_session(self) -> None:
        client = PolygonClient(api_key="test-key")
        with patch.object(client._session, "close") as mock_close:
            client.close()
        mock_close.assert_called_once()
