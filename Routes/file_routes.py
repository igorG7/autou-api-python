from fastapi import APIRouter ,File, Form, UploadFile, HTTPException
from typing import Optional
import io
from PyPDF2 import PdfReader

from services.llm_model import get_agent_response
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
        agent_response = get_agent_response(spacyTreatment(text_form), text_form)
        print(agent_response)
        return agent_response

  
    if not file:
        raise HTTPException(status_code=400, detail="Nenhuma informação arquivo foi enviado.")

    try:
        contents = await file.read()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao ler o arquivo: {e}")

    if file.content_type == "application/pdf":
        try:
            pdf_file = io.BytesIO(contents)
            reader = PdfReader(pdf_file)
            page = reader.pages[0]
            text = page.extract_text()
            
            print(agent_response)
            return agent_response
        except Exception:
            raise HTTPException(status_code=400, detail="Erro ao processar o arquivo PDF. Pode estar corrompido.")
    
    elif file.content_type == "text/plain":
        try:
            text = contents.decode("utf-8")
            agent_response = get_agent_response(spacyTreatment(text), text)
            print(agent_response)
            return agent_response
        except UnicodeDecodeError:
            raise HTTPException(status_code=400, detail="Erro ao decodificar arquivo de texto. Formato UTF-8 esperado.")

    else:
        raise HTTPException(status_code=400, detail="Formato de arquivo inválido. Apenas PDF ou TXT são aceitos.")

