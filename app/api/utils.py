from pydantic import ValidationError
from fastapi import HTTPException
from app.api.secret import SecretCreateRequest


def validate_secret_data(secret_data: dict):
    try:
        SecretCreateRequest(**secret_data)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=f"Invalid data: {e}")
