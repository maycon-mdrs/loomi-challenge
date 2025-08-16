from fastapi import FastAPI
from app.exceptions.exception_handlers import register_exception_handlers


app = FastAPI()
register_exception_handlers(app)


@app.get("/")
def health_check():
    return {"status": "ok"}
