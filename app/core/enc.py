from cryptography.fernet import Fernet
from app.core.config import settings

cipher_suite = Fernet(settings.encryption_secret_key)


def encrypt_secret(secret: str) -> str:
    """Шифрует секрет с использованием ключа."""
    encoded_secret = secret.encode('utf-8')
    encrypted_secret = cipher_suite.encrypt(encoded_secret)
    return encrypted_secret.decode('utf-8')


def decrypt_secret(encrypted_secret: str) -> str:
    """Дешифрует секрет с использованием ключа."""
    encrypted_secret_bytes = encrypted_secret.encode('utf-8')
    decrypted_secret = cipher_suite.decrypt(encrypted_secret_bytes)
    return decrypted_secret.decode('utf-8')
