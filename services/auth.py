import os
from fastapi import Header, HTTPException

API_SECRET = os.getenv("API_SECRET")


def verify_api_key(x_api_key: str = Header(None)):
    if x_api_key != API_SECRET:
        raise HTTPException(
            status_code=403,
            detail="Invalid API Key"
        )