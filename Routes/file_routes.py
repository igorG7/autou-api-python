from fastapi import APIRouter, UploadFile, File, Form
from PyPDF2 import PdfReader
from typing import Optional
import io
from utils.separate_text import separateText
from utils.spacy_treatment import spacyTreatment

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
        email_structure = separateText(text_form)
        teste = spacyTreatment(email_structure["conteúdo"])
        print(teste)
        return { "source": "form", "text": email_structure }
 
    contents = await file.read()

    if file.content_type == "application/pdf":
        pdf_file = io.BytesIO(contents)

        reader =  PdfReader(pdf_file)
        page = reader.pages[0]
        text = page.extract_text()

        email_structure = separateText(text)
        treated_text = spacyTreatment(email_structure["conteúdo"])
        print(treated_text)

        return { "source": "pdf", "filename": file.filename, "text": email_structure }
    
    if file.content_type == "text/plain":
        text = contents.decode("utf-8")
        email_structure = separateText(text)
        treated_text = spacyTreatment(email_structure["conteúdo"])
        print(treated_text)
        return { "source": "txt", "filename": file.filename, "text": text }
        

    return { "message": "Formato inválido ou nenhum arquivo foi enviado." }
