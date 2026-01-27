from datetime import datetime, timedelta, timezone
import jwt

SECRET_KEY = "79558f3b2c4d75eb04107d8981edb6fc717b68fb2914018e6a7f5a18b83d900efb1f4edaedb50787ce666a7d194393546f4cd7d9a88561b60d41c47ea0f281009c26df51edcd25153bc2c87c53e00e3f3a20f947288c21c435ce60db4ced99659d15277e6723fdfed4afd90ed2da4a09c92dcff2ec96aa5de1ccb0f2cccee2d79e08d8ab525fbbe303734b4152b3817e7657f95fb889e307ee7a9454d4a65cb"
ALGORITHM = "HS256"


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else: 
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"expire": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

