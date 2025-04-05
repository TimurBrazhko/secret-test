from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from app.models.secret import Secret, SecretLog, SecretResponse
from app.models.db import db_session
from app.cache.redis_cache import cache_secret, get_cached_secret
from app.core.enc import encrypt_secret, decrypt_secret
import uuid
import datetime

router = APIRouter()


class SecretCreateRequest(BaseModel):
    secret: str
    passphrase: str = None
    ttl_seconds: int = 3600


class SecretResponse(BaseModel):
    secret: str


@router.post("/secret")
async def create_secret(secret_data: SecretCreateRequest, request: Request):
    secret_key = str(uuid.uuid4())

    encrypted_secret = encrypt_secret(secret_data.secret)

    secret = Secret(
        secret_key=secret_key,
        secret=encrypted_secret,
        passphrase=secret_data.passphrase,
        ttl_seconds=secret_data.ttl_seconds,
        created_at=datetime.datetime.utcnow()
    )

    try:
        db_session.add(secret)
        db_session.commit()

        cache_secret(secret_key, encrypted_secret, secret_data.ttl_seconds)

        ip_address = request.client.host

        log_entry = SecretLog(
            secret_key=secret_key,
            action="created",
            ip_address=ip_address,
            ttl_seconds=secret_data.ttl_seconds,
            passphrase_used=secret_data.passphrase is not None,
            created_at=datetime.datetime.utcnow()
        )

        db_session.add(log_entry)
        db_session.commit()

        print(f"Secret created and logged. Secret key: {secret_key}, IP: {ip_address}")

        return {"secret_key": secret_key}

    except Exception as e:
        db_session.rollback()
        print(f"Error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/secret/{secret_key}", response_model=SecretResponse)
async def get_secret(secret_key: str, request: Request):
    secret_data = get_cached_secret(secret_key)

    if not secret_data:
        secret = db_session.query(Secret).filter_by(secret_key=secret_key).first()

        if not secret:
            raise HTTPException(status_code=404, detail="Secret not found")

        secret_data = decrypt_secret(secret.secret)

        cache_secret(secret_key, secret.secret, secret.ttl_seconds)

    ip_address = request.client.host
    log_message = f"Secret accessed. Key: {secret_key}, IP: {ip_address}"
    print(log_message)

    return SecretResponse(secret=secret_data)


@router.delete("/secret/{secret_key}")
async def delete_secret(secret_key: str, request: Request):
    secret = db_session.query(Secret).filter_by(secret_key=secret_key).first()

    if not secret:
        raise HTTPException(status_code=404, detail="Secret not found")

    db_session.delete(secret)
    db_session.commit()

    ip_address = request.client.host
    log_message = f"Secret deleted. Key: {secret_key}, IP: {ip_address}"
    print(log_message)


    return {"status": "secret_deleted"}
