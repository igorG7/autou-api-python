from fastapi import APIRouter, UploadFile, File, Form
from PyPDF2 import PdfReader
from typing import Optional
import io

from utils.send_content_agent import send_content_agent

file_router = APIRouter(prefix="/file", tags=["file"])

@file_router.post("/")

async def postFile(
    file: Optional[UploadFile] = File(None), 
    sender: Optional[str] = Form(None),  
    subject: Optional[str] = Form(None), 
    description: Optional[str] = Form(None)
    ): 

    if sender and subject and description:
        text_form = f"Remetente: {sender} \n Assunto: {subject} \n Conteúdo: {description}"
        response = await send_content_agent(text_form)
        print(response)
        return { "source": "form", "text": text_form }
 
    contents = await file.read()

    if file.content_type == "application/pdf":
        pdf_file = io.BytesIO(contents)

        reader =  PdfReader(pdf_file)
        page = reader.pages[0]
        text = page.extract_text()

        response = await send_content_agent(text)
        print(response)

        return { "source": "pdf", "filename": file.filename, "text": text }
    
    if file.content_type == "text/plain":
        text = contents.decode("utf-8")
        
        response = await send_content_agent(text)
        print(response)
       
        return { "source": "txt", "filename": file.filename, "text": text }
        

    return { "message": "Formato inválido ou nenhum arquivo foi enviado." }
