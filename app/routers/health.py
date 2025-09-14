from fastapi import APIRouter

router = APIRouter()


@router.get("/health", tags=["Health"])
async def health_check():
    """
    Performs a health check on the API.

    This endpoint is used to verify that the application is running and able to response to requests. It's a standard practice for monitoring and load balancing.

    Returns:
        dict: A dictionary with the status of the API.
            Example: {"status": "ok"}
    """
    return {"status": "ok"}
