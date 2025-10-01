from utils.separate_text import separateText
from utils.spacy_treatment import spacyTreatment
from services.llm_model import get_agent_response

async def send_content_agent(text: str):

    email_structure = separateText(text)
    treated_description = spacyTreatment(email_structure["conteúdo"])
    treated_subject = spacyTreatment(email_structure["assunto"])

    print(treated_description, treated_subject)
    response = get_agent_response(treated_description, treated_subject)
    return response
    