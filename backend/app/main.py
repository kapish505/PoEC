import app.patch
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import engine, Base
import app.models_orm

Base.metadata.create_all(bind=engine)

app = FastAPI(title="PoEC Anomaly Detection", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "PoEC Anomaly Detection Engine Ready"}

from app.api import routes
app.include_router(routes.router, prefix="/api/v1")
