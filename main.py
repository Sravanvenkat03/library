from fastapi import FastAPI
import uvicorn
from routing import router  # Ensure this module exists and has defined routes
from security_headers import SecurityHeadersMiddleware  # Ensure this middleware is defined
from pyinstrument_profiler import ProfilerMiddleware  # Ensure this middleware is installed

app = FastAPI()

#Add middleware
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(ProfilerMiddleware)

# Include the router
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
