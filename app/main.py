from fastapi import FastAPI
from app.api.secret import router as secret_router
from app.core.config import settings
from app.models.db import engine
from app.models.secret import Base
import uvicorn


app = FastAPI(
    title="One-Time Secrets Service",
    description="Сервис для хранения одноразовых конфиденциальных данных.",
    version="1.0.0"
)

Base.metadata.create_all(bind=engine)

app.include_router(secret_router, prefix="/secret", tags=["secrets"])


@app.get("/")
async def read_root():
    return {"message": "Одноразовый секрет"}

if __name__ == "__main__":
    uvicorn.run(app, host=settings.host, port=settings.port)
