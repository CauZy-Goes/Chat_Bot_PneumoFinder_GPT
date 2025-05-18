import os
import requests  # Para fazer requisições HTTP à sua API de tarefas
from flask import Flask, request  # Framework para criar a API que recebe mensagens do Twilio
from twilio.twiml.messaging_response import MessagingResponse  # Para responder mensagens no formato esperado pelo Twilio (WhatsApp)
from dotenv import load_dotenv  # Para carregar variáveis de ambiente do arquivo .env
from openai import OpenAI  # SDK oficial da OpenAI para chamar a API do ChatGPT
import json  # Para manipular dados JSON (decodificar e codificar)

# Carrega as variáveis de ambiente definidas no arquivo .env (exemplo: OPENAI_API_KEY)
load_dotenv()

app = Flask(__name__)  # Inicializa a aplicação Flask (servidor web)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  # Inicializa o cliente OpenAI com a chave da API
TASK_API_BASE = "http://localhost:8080/tasks"  # URL base da API de tarefas (para GET, POST, DELETE)
resp_erro = "Desculpe, tive um problema para responder. Por favor, tente novamente mais tarde."  # Mensagem padrão para erros

# Dicionário para armazenar o histórico de conversas por usuário (chave é o número do usuário)
historico_conversas = {}

MAX_HISTORICO = 20  # Limite máximo de mensagens mantidas no histórico para controle de tokens


# Função para listar tarefas fazendo uma requisição GET na API de tarefas
def listar_tarefas():
    resp = requests.get(TASK_API_BASE)  # Faz a requisição GET para obter tarefas
    if resp.status_code == 200:  # Se a resposta foi OK
        tarefas = resp.json()  # Converte o JSON para lista de tarefas
        if not tarefas:  # Se não há tarefas
            return "Sua lista de tarefas está vazia."
        texto = "Aqui estão suas tarefas:\n"
        for t in tarefas:
            texto += f"{t['id']}: {t['description']}\n"  # Monta texto listando id e descrição
        return texto
    else:
        # Caso a API não responda ou erro
        return "Não consegui acessar sua lista de tarefas agora."


# Função para adicionar uma tarefa, enviando POST para API com a descrição
def adicionar_tarefa(descricao):
    resp = requests.post(TASK_API_BASE, json={"description": descricao})
    if resp.status_code == 201:  # 201 Created indica sucesso
        return f"Tarefa '{descricao}' adicionada com sucesso!"
    else:
        return "Não consegui adicionar a tarefa no momento."


# Função para remover uma tarefa, enviando DELETE com o id da tarefa
def remover_tarefa(id_str):
    try:
        id_task = int(id_str)  # Converte o id recebido para inteiro
    except ValueError:
        return "O id da tarefa deve ser um número."  # Se não for número, retorna erro amigável

    resp = requests.delete(f"{TASK_API_BASE}/{id_task}")  # DELETE para o endpoint específico
    if resp.status_code == 204:  # 204 No Content = sucesso na exclusão
        return f"Tarefa {id_task} removida com sucesso."
    elif resp.status_code == 404:  # Se tarefa não foi encontrada
        return f"Tarefa {id_task} não encontrada."
    else:
        return "Não consegui remover a tarefa no momento."


# Função que manda a mensagem do usuário para o GPT para interpretar qual comando ele quer executar,
# e receber o comando em JSON para facilitar o processamento depois
def obter_comando_gpt(mensagem_usuario, sender):
    if sender not in historico_conversas:
        historico_conversas[sender] = []

    # Prompt que define que o GPT deve responder SOMENTE JSON válido, indicando qual ação executar
    system_prompt = (
        "Você é um assistente que interpreta comandos para gerenciar tarefas. Além de ser o assistente você manipula a lista de tarefas do usuário"
        "Tu pode, adicionar, remover e listar as tarefas do usuário"
        "Quando o usuário enviar uma mensagem, responda SOMENTE um JSON válido com a seguinte estrutura:\n"
        "- Para listar tarefas: {\"action\": \"list\"}\n"
        "- Para adicionar tarefa: {\"action\": \"add\", \"description\": \"<descrição>\"}\n"
        "- Para remover tarefa: {\"action\": \"remove\", \"id\": <id>}\n"
        "- Se a mensagem não for para a lista de tarefas, responda: {\"action\": \"chat\", \"content\": \"<resposta natural>\"}\n"
        "Não adicione texto extra, apenas JSON válido."
    )

    mensagens = [{"role": "system", "content": system_prompt}]
    mensagens.append({"role": "user", "content": mensagem_usuario})

    # Chama a API do GPT para obter o comando JSON
    resposta = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=mensagens,
        temperature=0.85,  # temperatura zero para respostas mais precisas e previsíveis
        max_tokens=150,
    )

    conteudo = resposta.choices[0].message.content.strip()

    try:
        comando = json.loads(conteudo)  # Tenta transformar o texto JSON em dicionário Python
        return comando
    except json.JSONDecodeError:
        # Se o GPT não retornou JSON válido, volta uma ação genérica de chat com o texto recebido
        return {"action": "chat", "content": conteudo}


# Função principal para gerar a resposta final que será enviada para o usuário no WhatsApp
def gerar_resposta(sender, mensagem_usuario):
    # Pega o comando interpretado pelo GPT (JSON)
    comando = obter_comando_gpt(mensagem_usuario, sender)

    # Executa a ação conforme o comando retornado
    if comando["action"] == "list":
        resultado_api = listar_tarefas()
    elif comando["action"] == "add":
        descricao = comando.get("description", "")
        if descricao:
            resultado_api = adicionar_tarefa(descricao)
        else:
            resultado_api = "Descrição da tarefa não informada para adicionar."
    elif comando["action"] == "remove":
        id_task = comando.get("id", None)
        if id_task is not None:
            resultado_api = remover_tarefa(str(id_task))
        else:
            resultado_api = "ID da tarefa para remoção não informado."
    elif comando["action"] == "chat":
        # Se for só conversa, já retorna o conteúdo direto sem acessar API
        return comando["content"]
    else:
        resultado_api = "Não entendi a ação solicitada."

    # Agora, para deixar a resposta mais natural, pede para o GPT gerar um texto com base no resultado da API
    system_prompt = "Você é um assistente digital prestativo e educado."
    user_prompt = (
        "Você é um assistente que interpreta comandos para gerenciar tarefas. Além de ser o assitente você manipula a lista de tarefas do usuário"
        "Tu pode, adicionar, remover e listar as tarefas do usuário"
        f"O usuário enviou: {mensagem_usuario}\n"
        f"O resultado da ação na API foi: {resultado_api}\n"
        "Responda para o usuário de forma clara e amigável."
    )

    mensagens = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    resposta_final = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=mensagens,
        temperature=0.7,
        max_tokens=200,
    )

    resposta_texto = resposta_final.choices[0].message.content.strip()

    # Guarda no histórico do usuário (mantendo o contexto para futuras mensagens)
    if sender not in historico_conversas:
        historico_conversas[sender] = []
    historico_conversas[sender].append({"role": "user", "content": mensagem_usuario})
    historico_conversas[sender].append({"role": "assistant", "content": resposta_texto})

    # Limita o tamanho do histórico para evitar problemas de limite de tokens na API
    historico_conversas[sender] = historico_conversas[sender][-MAX_HISTORICO:]

    return resposta_texto


# Endpoint que recebe as mensagens via webhook do Twilio (WhatsApp)
@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.form.get('Body').strip()  # Texto da mensagem recebida
    sender = request.form.get('From')  # Número do remetente da mensagem
    print(f"Mensagem de {sender}: {incoming_msg}")

    resp = MessagingResponse()  # Objeto para montar a resposta em formato Twilio

    try:
        resposta_gerada = gerar_resposta(sender, incoming_msg)  # Gera resposta usando toda lógica acima
        resp.message(resposta_gerada)  # Adiciona a mensagem para responder ao usuário
    except Exception as e:
        print(f"Erro ao gerar resposta: {e}")
        resp.message(resp_erro)  # Em caso de erro, envia mensagem padrão

    print(f"Resposta do bot: {resposta_gerada}")
    return str(resp)  # Retorna a resposta para o Twilio (XML)


# Executa o servidor Flask no modo debug localmente
if __name__ == "__main__":
    app.run(debug=True)
