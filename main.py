from fastapi import FastAPI
from routes.file_routes import file_router

app = FastAPI()

app.include_router(file_router)