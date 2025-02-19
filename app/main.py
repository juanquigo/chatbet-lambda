from fastapi import FastAPI
from mangum import Mangum

from app.routers.provider import router as provider_router
from app.settings import get_settings

settings = get_settings()
app = FastAPI(title=settings["app_name"])
app.include_router(provider_router)
handler = Mangum(app)
