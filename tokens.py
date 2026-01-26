from datetime import datetime, timedelta, timezone

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()