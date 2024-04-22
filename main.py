from fastapi import FastAPI
from starlette.middleware.authentication import AuthenticationMiddleware

from users.routes import router as guest_router, user_router
from auth.route import router as auth_router
from core.security import JWTAuth



app = FastAPI(
    title="FastAPI Auth",
    description="This is a sample API",
    version="0.1.0",
    docs_url="/",
    redoc_url="/redoc",
)


app.include_router(guest_router)
app.include_router(user_router)
app.include_router(auth_router)

# Middleware
app.add_middleware(AuthenticationMiddleware, backend=JWTAuth())