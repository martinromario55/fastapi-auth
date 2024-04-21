from fastapi import FastAPI

from users.routes import router as user_router



app = FastAPI(
    title="FastAPI Auth",
    description="This is a sample API",
    version="0.1.0",
    docs_url="/",
    redoc_url="/redoc",
)

app.include_router(user_router)
