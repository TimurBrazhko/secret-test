import logging
from app.logs.log_config import configure_logging

configure_logging()

logger = logging.getLogger()


def log_secret_creation(secret_key: str, ip_address: str, ttl_seconds: int):
    """Логирование создания секрета."""
    logger.info(f"Secret created with key: {secret_key}, IP: {ip_address}, TTL: {ttl_seconds} seconds")


def log_secret_access(secret_key: str, ip_address: str):
    """Логирование доступа к секрету."""
    logger.info(f"Secret accessed with key: {secret_key}, IP: {ip_address}")


def log_secret_deletion(secret_key: str, ip_address: str, passphrase_used: bool):
    """Логирование удаления секрета."""
    logger.info(f"Secret deleted with key: {secret_key}, IP: {ip_address}, Passphrase used: {passphrase_used}")
