import os
from datetime import timedelta

from fastapi_jwt import JwtAccessBearerCookie, JwtRefreshBearerCookie


class JWTConfig:
    refresh_expires_delta = timedelta(days=30)
    access_expires_delta = timedelta(minutes=15)
    secret = os.getenv("JWT_SECRET") or "abababababa"

    refresh_security = JwtRefreshBearerCookie(
        auto_error=True,
        secret_key=secret,
        access_expires_delta=refresh_expires_delta,
    )
    access_security = JwtAccessBearerCookie(
        auto_error=True,
        secret_key=secret,
        access_expires_delta=access_expires_delta
    )


jwt_config = JWTConfig
