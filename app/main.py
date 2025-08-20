from fastapi import FastAPI
from app.config import API_PREFIX
from app.exceptions.exception_handlers import register_exception_handlers
from app.routes.chat_router import chat_router
from app.routes.auth_router import auth_router
from app.routes.paint_router import paint_router
from app.routes.user_router import user_router


app = FastAPI()
register_exception_handlers(app)


@app.head("/", tags=["Health Check"])
def health_check():
    return {"status": "ok"}


app.include_router(auth_router, prefix=API_PREFIX)
app.include_router(chat_router, prefix=API_PREFIX)
app.include_router(user_router, prefix=API_PREFIX)
app.include_router(paint_router, prefix=API_PREFIX)
