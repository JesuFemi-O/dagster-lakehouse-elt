from fastapi import HTTPException, Header
import os

API_KEY = os.environ.get("API_KEY", "mysecretkey")

def verify_api_key(x_api_key: str = Header(...)):
    """Verify the API key."""
    if x_api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")
    return x_api_key
