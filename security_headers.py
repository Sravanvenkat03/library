import os
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
 
is_production = os.getenv("ENVIRONMENT") == "production"
 
class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response: Response = await call_next(request)
       
        # Apply security headers only in production
        if is_production:
            if request.url.path.startswith("/docs") or request.url.path.startswith("/redoc"):
                response.headers["Content-Security-Policy"] = (
                    "default-src 'self'; "
                    "script-src 'self' 'unsafe-inline' 'unsafe-eval'; "
                    "style-src 'self' 'unsafe-inline';"
                )
            else:
                response.headers["Content-Security-Policy"] = "default-src 'self';"
                response.headers["X-Content-Type-Options"] = "nosniff"
                response.headers["X-Frame-Options"] = "DENY"
                response.headers["Strict-Transport-Security"] = "max-age=63072000; includeSubDomains; preload"
                response.headers["X-XSS-Protection"] = "0"
                response.headers["Referrer-Policy"] = "no-referrer"
 
        return response