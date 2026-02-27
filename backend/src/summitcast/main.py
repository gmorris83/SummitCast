from fastapi import FastAPI
from summitcast.api.router import api_router

app = FastAPI(
    title="SummitCast API",
    version="0.1.0"
)

@app.get("/")
def root():
    return {"message": "SummitCast API running"}

app.include_router(api_router, prefix="/api")