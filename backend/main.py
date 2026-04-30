from fastapi import FastAPI, Body, Query
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from orchestrator import process_requirement
from config import settings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="AI Dev Agent Pro")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.on_event("startup")
async def startup():
    try:
        settings.validate()
        logger.info("Configuration validated")
    except ValueError as e:
        logger.error(f"Config error: {e}")

@app.get("/health")
async def health():
    return {"status": "ok", "model": settings.model}

@app.post("/generate")
async def generate_post(requirement: str = Body(...)):
    return StreamingResponse(
        process_requirement(requirement),
        media_type="text/event-stream"
    )

@app.get("/generate")
async def generate_get(requirement: str = Query(...)):
    return StreamingResponse(
        process_requirement(requirement),
        media_type="text/event-stream"
    )
