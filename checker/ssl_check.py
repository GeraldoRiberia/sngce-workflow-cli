import ssl
import socket
from datetime import datetime, timezone


def check_ssl(hostname: str, port: int = 443, timeout: int = 10) -> dict:
    """
    Checks the SSL certificate expiry for a given hostname.
    Returns a dict with: valid, days_remaining, expires_on, error
    """
    # Strip scheme if present
    hostname = hostname.replace("https://", "").replace("http://", "").rstrip("/")
    # Strip any path
    hostname = hostname.split("/")[0]

    result = {
        "hostname": hostname,
        "valid": False,
        "days_remaining": None,
        "expires_on": None,
        "error": None,
    }

    try:
        context = ssl.create_default_context()
        with socket.create_connection((hostname, port), timeout=timeout) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()

        expire_str = cert["notAfter"]  # e.g. 'Sep 10 12:00:00 2025 GMT'
        expire_dt = datetime.strptime(expire_str, "%b %d %H:%M:%S %Y %Z").replace(tzinfo=timezone.utc)
        now = datetime.now(timezone.utc)
        days_remaining = (expire_dt - now).days

        result["valid"] = days_remaining > 0
        result["days_remaining"] = days_remaining
        result["expires_on"] = expire_dt.strftime("%Y-%m-%d")

    except ssl.SSLCertVerificationError as e:
        result["error"] = f"SSL verification failed: {e}"
    except ssl.SSLError as e:
        result["error"] = f"SSL error: {e}"
    except socket.timeout:
        result["error"] = f"Timed out after {timeout}s"
    except ConnectionRefusedError:
        result["error"] = "Connection refused on port 443"
    except Exception as e:
        result["error"] = str(e)

    return result
