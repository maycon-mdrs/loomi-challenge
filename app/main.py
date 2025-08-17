from fastapi import FastAPI
from app.exceptions.exception_handlers import register_exception_handlers
from app.routes.auth_router import auth_router
from app.routes.paint_router import paint_router
from app.routes.user_router import user_router

API_PREFIX = "/api/v1"

app = FastAPI()
register_exception_handlers(app)


@app.head("/", tags=["Health Check"])
def health_check():
    return {"status": "ok"}


app.include_router(auth_router, prefix=API_PREFIX)
app.include_router(user_router, prefix=API_PREFIX)
app.include_router(paint_router, prefix=API_PREFIX)
