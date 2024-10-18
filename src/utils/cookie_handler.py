from datetime import datetime, timedelta
from typing import Optional

from flask import Response, current_app, request


def set_cookie(
    response: Response, key: str, value: str, max_age: Optional[int] = None
) -> None:
    """Set a cookie with the given key and value."""
    if max_age is None:
        max_age = int(current_app.config["COOKIE_LIFETIME"].total_seconds())
    expires = datetime.now() + timedelta(seconds=max_age)
    response.set_cookie(
        key,
        value,
        max_age=max_age,
        expires=expires,
        httponly=True,
        secure=current_app.config["SESSION_COOKIE_SECURE"],
        samesite="Lax",
    )


def get_cookie(key: str) -> Optional[str]:
    """Get the value of a cookie by its key."""
    return request.cookies.get(key)


def delete_cookie(response: Response, key: str) -> None:
    """Delete a cookie by its key."""
    response.delete_cookie(key)
