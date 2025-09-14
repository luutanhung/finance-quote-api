from fastapi import APIRouter, Request

from app.core.rate_limiter import limiter

router = APIRouter()


@router.get("/health", tags=["Health"])
@limiter.exempt
async def health_check(request: Request):
    """
    Performs a health check on the API.

    This endpoint is used to verify that the application is running and able to response to requests. It's a standard practice for monitoring and load balancing.

    Returns:
        dict: A dictionary with the status of the API.
            Example: {"status": "ok"}
    """

    return {"status": "ok"}
