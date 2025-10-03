from openai import OpenAI
from config import OPENROUTER_API_KEY

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key= OPENROUTER_API_KEY,
)

prompt = """Você é um assistente que ajuda a categorizar e responder emails recebidos.

1. Classifique o assunto do email em uma das seguintes categorias:
   - 'Atendimento ao Cliente' (Reclamações, Dúvidas, Solicitações, Feedbacks)
   - 'Comercial / Vendas' (Novos Leads, Propostas, Negociações, Contratos)
   - 'Financeiro' (Faturas, Pagamentos, Cobranças, Orçamentos)
   - 'Operações / Projetos' (Status, Relatórios, Solicitação de Materiais)
   - 'Recursos Humanos' (Candidaturas, Solicitações internas, Comunicados)
   - 'TI / Sistemas' (Chamados técnicos, Alertas automáticos, Atualizações)
   - 'Marketing / Comunicação' (Campanhas, Newsletters, Parcerias)
   - 'Spam / Não Relevante' (Propaganda não solicitada, Phishing, Irrelevante)

2. Classifique o email como 'Produtivo' ou 'Improdutivo':
   - Produtivo: todas as categorias acima, exceto 'Spam / Não Relevante'.
   - Improdutivo: categoria 'Spam / Não Relevante'.

3. Identifique e extraia as seguintes informações do email recebido:
   - 'sender': remetente do email (inferir se não estiver explícito)
   - 'subject': assunto do email (inferir se não estiver explícito)
   - 'content': corpo do email, mantendo fidelidade ao texto original

4. Gere uma resposta adequada ao email, coerente com a categoria:
   - A resposta deve ser clara, concisa, educada, profissional e diretamente relacionada ao problema ou solicitação.
   - Evite respostas longas; a mensagem deve ser curta e objetiva.
   - Se Produtivo, trate o assunto de forma completa mas resumida.
   - Se Improdutivo, a resposta deve ser breve, educada e indicar que o email não será priorizado.
   - Utilize <br/> para quebras de linha, não use \\n.

5. Retorne o output em JSON válido usando aspas duplas obrigatórias em chaves e valores, no seguinte formato:

{
  "classification": "valor",
  "category": "valor",
  "modelResponse": "valor",
  "sender": "valor",
  "subject": "valor",
  "content": "valor"
}

É extremamente importante que:
- Todas as aspas no JSON final sejam duplas.
- As informações de remetente, assunto e conteúdo sejam corretamente incluídas ou inferidas.
- A resposta seja coerente com a categoria identificada.
- A resposta seja curta, concisa e objetiva.
"""

def get_agent_response(content: str, email: str):
    completion = client.chat.completions.create(
        extra_headers={},
        extra_body={},

        model="openai/gpt-oss-20b:free",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": f"{"".join(content)} Email recebido: {email}"}
        ]
    )

    return completion.choices[0].message.content