from typing import Any
from fastapi import status
from fastapi.responses import JSONResponse


class AppException(Exception):
    status_code: int = status.HTTP_400_BAD_REQUEST
    message: str = "An error occurred"

    def __init__(self, detail: Any = None):
        self.detail = detail or {"message": self.message}

    def response(self):
        return JSONResponse(status_code=self.status_code, content=self.detail)
