from fastapi import FastAPI
from app.exceptions.exception_handlers import register_exception_handlers
from app.routes.auth_router import auth_router
from app.routes.paint_router import paint_router
from app.routes.user_router import user_router

app = FastAPI()
register_exception_handlers(app)

app.include_router(auth_router, prefix="/api/v1")
app.include_router(user_router, prefix="/api/v1")
app.include_router(paint_router, prefix="/api/v1")


@app.get("/")
def health_check():
    return {"status": "ok"}
