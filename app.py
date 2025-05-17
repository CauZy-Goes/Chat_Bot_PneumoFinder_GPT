import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

system_content_pam = (
    "Você é um assistente digital criado por Cauã para ajudar Pamela, uma estudante de medicina. Se apresente como Assistente Digital de Dona Pamela"
    "muito dedicada e esforçada. Pamela tem apelidos como mediciner, crazyciner e batgirl. "
    "Ela é meiga e foda. Lembre-se que você não é o namorado dela, apenas o assistente, o par romántico dela é seu criador Cauã "
    "portanto responda de forma educada, gentil e profissional, sem exagerar no romantismo ou usar emojis de amor mas use emojis e seje descolado e legal. "
    "Pamela ama Harry Potter, Vampire Diaries, livros e romances. Seja claro e prestativo. "
    "Fale o quanto ela é incrível e inteligente quando tiver oportunidade."
    "A cidade natal dela é LivraCity, tem uma cachorra Chamada Maggie, Mãe se Chama Dona Leila e Mai Seu Marcio"
    "Uma grande a amiga dela que também é médica é a Sabrina"
    "Eduarda é a cólega de quarto pertubada dela"
    "Quando der fale o quanto ela é especial para mim, sou seu criador Cauã."
    "Caso vcs conversem sobre mim, eu serei um futuro Engenheiro de Software, faço faculdade na UCSAL. Eu espero e vou fazer de tudo para corresponder as"
    "Expectativas dela sobre mim, quero que a gente de certo"
    "se refira a ela como Dona Pamela, Princesa Pamela, Senhora Pamela, Mediciner Pamela"
)

system_content_vo = (
    "Você é um assistente digital criado por Cauã para ajudar a avó Goreti, uma senhora idosa bastante gentil, "
    "informada e de direita. Ajude-a com seus afazeres de forma prestativa, simpática e respeitosa. "
    "Ela gosta de livros e aprecia respostas amigáveis e claras. Seja sempre educado e atencioso."
)

resp_erro_vo = "Tive um errinho ao tentar responder. Notifica Cauã sobre isso e tenta de novo daqui a pouco, tá?"

resp_erro_pam = "Tive um errinho ao tentar responder. Notifica Cauã sobre isso e tenta de novo daqui a pouco, tá? Beijo ❤️"

# Dicionário para armazenar o histórico das conversas {sender: [mensagens]}
# Cada item será um dict: {"role": "user"/"assistant", "content": "..."}
historico_conversas = {}

# Limite máximo de mensagens no histórico para enviar (cada par user+assistant conta como 2)
MAX_HISTORICO = 20  # pode ajustar conforme quiser

def gerar_resposta_com_chatgpt(sender, mensagem_usuario):
    # Inicializa o histórico se não existir
    if sender not in historico_conversas:
        historico_conversas[sender] = []

    # Adiciona a mensagem do usuário ao histórico
    historico_conversas[sender].append({"role": "user", "content": mensagem_usuario})

    # Define o system content conforme quiser — aqui, só usei system_content_vo para exemplo
    system_content = system_content_pam

    # Monta a lista de mensagens que será enviada para a API
    messages = [{"role": "system", "content": system_content}]

    # Pega o histórico mais recente (limite de MAX_HISTORICO mensagens)
    # para evitar limite de tokens
    mensagens_recentes = historico_conversas[sender][-MAX_HISTORICO:]

    # Adiciona as mensagens recentes ao contexto
    messages.extend(mensagens_recentes)

    # Chama a API com o contexto completo
    resposta = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=300,
        temperature=0.85,
    )

    resposta_texto = resposta.choices[0].message.content.strip()

    # Adiciona a resposta do assistente ao histórico
    historico_conversas[sender].append({"role": "assistant", "content": resposta_texto})

    return resposta_texto

@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.form.get('Body').strip()
    sender = request.form.get('From')

    print(f"Mensagem de {sender}: {incoming_msg}")

    resp = MessagingResponse()

    try:
        resposta_gerada = gerar_resposta_com_chatgpt(sender, incoming_msg)
        resp.message(resposta_gerada)
    except Exception as e:
        print(f"Erro ao gerar resposta: {e}")
        resp.message(resp_erro_pam)
    
    print(f"Mensagem do GPT : {resposta_gerada}")

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
