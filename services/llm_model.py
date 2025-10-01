from openai import OpenAI
from config import OPENROUTER_API_KEY

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key= OPENROUTER_API_KEY,
)

prompt = "Você é um assistente que ajuda a categorizar e responder emails recebidos. Classifique o assunto do email como 'Produtivo' ou 'Improdutivo' analisando o tópico informado. Após classificar, gere uma resposta adequada para o email baseada no conteúdo fornecido. A resposta deve ser clara, concisa e relevante para o conteúdo do email e deve ajudar a resolver o problema ou fornecer informações úteis. Certifique-se de que a resposta seja educada e profissional. Se o email for categorizado como 'Improdutivo', a resposta deve ser breve e indicar que o email não será priorizado. Se for 'Produtivo', a resposta deve abordar diretamente o problema ou questão levantada no email. Envie como resposta um dicionario no seguinte formato: {'categoria': 'Produtivo' ou 'Improdutivo', 'resposta': 'sua resposta aqui'}."


def get_agent_response(description: str, subject: str):
    completion = client.chat.completions.create(
        extra_headers={},
        extra_body={},

        model="openai/gpt-oss-20b:free",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": f"Assunto: {"".join(subject)} Conteúdo: {"".join(description)}"}
        ]
    )

    return completion.choices[0].message.content