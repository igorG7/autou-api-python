from fastapi import APIRouter, UploadFile, File, Form

file_router = APIRouter(prefix="/file", tags=["file"])