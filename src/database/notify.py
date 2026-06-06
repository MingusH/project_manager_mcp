"""Notification utility for MCP tools to trigger dashboard updates."""

import urllib.request
import urllib.error
import json
import os


def notify_dashboard(update_type: str = "refresh") -> None:
    """Notify dashboard API of data changes via internal endpoint."""
    api_url = os.getenv("DASHBOARD_API_URL", "http://dashboard-api:8000")
    url = f"{api_url}/internal/notify?update_type={update_type}"
    
    try:
        req = urllib.request.Request(
            url,
            data=b"",
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        urllib.request.urlopen(req, timeout=2)
    except urllib.error.URLError:
        pass  # Dashboard API might not be running
    except Exception:
        pass  # Any other error, ignore silently
