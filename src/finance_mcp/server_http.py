"""
Finance MCP Server — FastMCP streamable-http transport.

This is the HTTP entry point for claude.ai remote connections.
It reuses the same FastMCP instance from server.py — all tools are
already registered. Only the transport differs.

Run:  python -m finance_mcp.server_http [port]
Default port: 8000
Endpoint: http://0.0.0.0:{port}/mcp

IMPORTANT: Do NOT modify server.py to add HTTP transport.
The stdio server must remain unchanged for Claude Code via .mcp.json.
"""
import sys

from finance_mcp.server import mcp


def start(port: int = 8000) -> None:
    """Start the finance MCP server with streamable-http transport."""
    print(f"[finance-mcp] Starting HTTP server on port {port}", file=sys.stderr)
    print(f"[finance-mcp] Endpoint: http://0.0.0.0:{port}/mcp", file=sys.stderr)
    mcp.run(transport="streamable-http", host="0.0.0.0", port=port)


if __name__ == "__main__":
    _port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    start(_port)
