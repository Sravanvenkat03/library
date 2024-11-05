from fastapi import FastAPI, Request
from pyinstrument import Profiler
import logging
from starlette.middleware.base import BaseHTTPMiddleware

logging.basicConfig(level=logging.INFO)

class ProfilerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        profiler = Profiler()
        profiler.start()

        response = await call_next(request)

        profiler.stop()
        logging.info(profiler.output_text(unicode=True, color=True))
        endpoint = request.url.path.replace('/', '_')
        with open(f"memory_profile_{endpoint}.html", "w") as f:
            f.write(profiler.output_html())

        return response
