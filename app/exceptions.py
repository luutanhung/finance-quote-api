from fastapi import HTTPException, status
from fastapi.responses import JSONResponse


class NotFound(HTTPException):
    def __init__(self, detail: str = "Not Found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


async def not_found_handler(request, exc: NotFound):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND, content={"detail": str(exc)}
    )
