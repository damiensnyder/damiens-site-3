"""First-party submission telemetry.

Lightweight, no third-party services: form-submission attempts are written to a
rotating log file (configured under LOGGING['handlers']['submissions_file'] in
settings.py) so abusive user-agents / IPs can be spotted after the fact.
"""

import logging

logger = logging.getLogger("submissions")


def client_ip(request):
    """Best-effort client IP.

    Honors X-Forwarded-For since the site runs behind a proxy. XFF is
    client-spoofable unless the edge proxy overwrites it, but this is telemetry
    only, so the left-most reported value is good enough.
    """
    xff = request.META.get("HTTP_X_FORWARDED_FOR")
    if xff:
        return xff.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR", "")


def log_submission(request, event, **extra):
    """Record a form-submission attempt. Never raises — telemetry must not break
    the request flow."""
    try:
        ua = request.META.get("HTTP_USER_AGENT", "")
        details = " ".join(f"{k}={v}" for k, v in extra.items())
        logger.info(
            "event=%s ip=%s path=%s ua=%r %s",
            event, client_ip(request), request.path, ua, details,
        )
    except Exception:
        pass
