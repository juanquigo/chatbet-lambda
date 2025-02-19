from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from mangum import Mangum

from app.routers.provider import router as provider_router
from app.settings import get_settings

settings = get_settings()
app = FastAPI(title=settings["app_name"])


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_: Request, exc: RequestValidationError) -> JSONResponse:
    """Handle validation errors and return a JSON response with error details.

    Args:
        _ (Request): The request object (not used).
        exc (RequestValidationError): The validation error exception.

    Returns:
        JSONResponse: A JSON response with the error details and a 400 status code.

    """
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": exc.errors()},
    )


app.include_router(provider_router)
handler = Mangum(app)
