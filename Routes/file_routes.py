from fastapi import APIRouter, File, Form, UploadFile, HTTPException
from typing import Optional
import io
from PyPDF2 import PdfReader

file_router = APIRouter(prefix="/file", tags=["file"])

from services.llm_model import get_agent_response
from utils.spacy_treatment import spacyTreatment

@file_router.post("/")
async def postFile(
    file: Optional[UploadFile] = File(None), 
    sender: Optional[str] = Form(None),  
    subject: Optional[str] = Form(None), 
    description: Optional[str] = Form(None)
): 
    # Prioriza o processamento do formulário de texto, se todos os campos estiverem preenchidos.
    if sender and subject and description:
        text_form = f"Remetente: {sender} \n Assunto: {subject} \n Conteúdo: {description}"
        agent_response = get_agent_response(spacyTreatment(text_form), text_form)
        print(agent_response)
        return agent_response

    # Trata o caso em que nenhum arquivo foi enviado.
    if not file:
        raise HTTPException(status_code=400, detail="Nenhum arquivo foi enviado.")

    # Tenta ler o conteúdo do arquivo com tratamento de exceções.
    try:
        contents = await file.read()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao ler o arquivo: {e}")

    # Processa o arquivo com base no seu tipo, usando try...except.
    if file.content_type == "application/pdf":
        try:
            pdf_file = io.BytesIO(contents)
            reader = PdfReader(pdf_file)
            page = reader.pages[0]
            text = page.extract_text()
            
            agent_response = get_agent_response(spacyTreatment(text), text)
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

    # Retorna um erro se o formato do arquivo não for compatível.
    else:
        raise HTTPException(status_code=400, detail="Formato de arquivo inválido. Apenas PDF ou TXT são aceitos.")

