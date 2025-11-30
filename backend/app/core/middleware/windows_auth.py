from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

class WindowsAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        user = request.headers.get("X-Forwarded-User")
        if user:
            request.state.windows_user = user
        else:
            request.state.windows_user = None
        response = await call_next(request)
        return response