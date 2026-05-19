import requests
import time


def check_backend(url: str, health_endpoint: str = "/health", timeout: int = 10) -> dict:
    """
    Pings the backend health endpoint and returns status info.
    Returns a dict with: reachable, status_code, response_time_ms, error
    """
    full_url = url.rstrip("/") + health_endpoint
    result = {
        "url": full_url,
        "reachable": False,
        "status_code": None,
        "response_time_ms": None,
        "error": None,
    }

    try:
        start = time.monotonic()
        response = requests.get(full_url, timeout=timeout)
        elapsed = (time.monotonic() - start) * 1000

        result["reachable"] = True
        result["status_code"] = response.status_code
        result["response_time_ms"] = round(elapsed, 1)

        # Treat anything outside 200-299 as degraded, not down
        if not response.ok:
            result["error"] = f"Non-OK status: {response.status_code}"

    except requests.exceptions.ConnectionError:
        result["error"] = "Connection refused or host unreachable"
    except requests.exceptions.Timeout:
        result["error"] = f"Timed out after {timeout}s"
    except requests.exceptions.RequestException as e:
        result["error"] = str(e)

    return result
