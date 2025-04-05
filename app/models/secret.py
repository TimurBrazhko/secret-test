from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()


class Secret(Base):
    __tablename__ = "secrets"

    secret_key = Column(String, primary_key=True, index=True)
    secret = Column(String, nullable=False)
    passphrase = Column(String, nullable=True)
    ttl_seconds = Column(Integer, default=3600)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Связь с SecretLog
    secret_logs = relationship("SecretLog", back_populates="secret", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Secret(secret_key={self.secret_key}, created_at={self.created_at}, ttl_seconds={self.ttl_seconds})>"


class SecretLog(Base):
    __tablename__ = "secret_logs"

    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    secret_key = Column(String, ForeignKey("secrets.secret_key"), nullable=False)
    action = Column(String, nullable=False)
    ip_address = Column(String, nullable=False)
    ttl_seconds = Column(Integer, nullable=True)
    passphrase_used = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    secret = relationship("Secret", back_populates="secret_logs")

    def __repr__(self):
        return f"<SecretLog(secret_key={self.secret_key}, action={self.action}, ip_address={self.ip_address})>"


from pydantic import BaseModel
from typing import Optional


class SecretCreateRequest(BaseModel):
    secret: str
    passphrase: Optional[str] = None
    ttl_seconds: Optional[int] = None


class SecretResponse(BaseModel):
    secret: str
