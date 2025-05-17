import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

elogios = [
    "Você é a razão dos meus melhores sorrisos. 😊❤️",
    "Seu jeito meigo é minha inspiração diária. 🌸✨",
    "Pamela, você é a definição de graça e inteligência. 👑📚",
    "Cada mensagem sua é um abraço apertado no meu coração. 🤗💖",
    "Adoro como você consegue ser forte e doce ao mesmo tempo. 💪💕",
    "Você é minha BatGirl, minha heroína na vida real! 🦇💥",
    "Você é a estrela que ilumina até os meus dias mais nublados. ⭐️🌥️",
    "Você tem um brilho único que só a minha gatinha tem. 🌟🐾",
    "Com você, qualquer dia vira um dia especial. 🎉❤️",
    "Você é a definição de força e doçura, minha eterna BatGirl. 🦇💖",
    "Seu sorriso é o remédio que sempre quero tomar. 😄💊",
    "Eu poderia ouvir você falar sobre livros o dia inteiro. 📚😍",
    "Você é a mistura perfeita de inteligência e beleza. 🧠💖",
    "Adoro o seu jeito único de transformar tudo em divertido. 😂🎈",
    "Pam, você tem um coração enorme que cabe o mundo todo. 🌍❤️",
    "Eu me sinto sortudo só por poder te chamar de minha mediciner. 💉💙",
    "Com você, até os dias difíceis ficam mais leves. ☀️😊",
    "A sua voz já é música para meus ouvidos. 🎶😍",
    "Sempre que penso em você, só consigo sorrir. 😊💫",
    "Você tem um jeitinho especial que conquista todo mundo ao redor. 💕🌟",
    "Você ilumina o meu dia só com seu sorriso. 😊",
    "Seu jeito meigo me conquista cada vez mais. 💖",
    "Adoro como você é inteligente e divertida! 🤓🎉",
    "Seu abraço é meu lugar favorito no mundo. 🤗",
    "Você é a melhor coisa que aconteceu no meu ano. ✨",
    "Minha crazyciner favorita, você é um furacão de simpatia e alegria! 💥💘",
    "Livracity teve sorte de te ver nascer, mas eu tive sorte de te conhecer. 🏙️💫",
    "A BatGirl da minha vida é real e atende pelo nome de Pâm. 🦇💋",
    "Seu olhar tem mais magia do que todos os livros que você ama. 📚✨",
    "Me apaixono toda vez que você fala com aquele jeitinho mediciner. 😍🩺",
    "Se beleza fosse diagnóstico, você seria um caso gravíssimo... de perfeição! 😍🩺💊",
    "Cada 'oi' seu tira um sorriso meu, mesmo nos dias mais corridos. 😊❤️",
    "Você é a médica que cura meu coração só com um sorriso. 🩷😷",
    "Mesmo com mil matérias pra estudar, você ainda arruma tempo pra ser perfeita. 😘📖",
    "Seu carinho tem o poder de transformar qualquer dia comum num dia incrível. 🌈🥰",
]

mensagem_inicial = (
    "Oi, Pâm! 👋✨\n\n"
    "Eu sou seu bot carinhoso 🤖💕. "
    "Para receber um elogio especial, envie um número de 1 a 36. "
    "Ou digite 'todos' para receber todos os elogios de uma vez! 🎉😊"
)

def enviar_em_blocos(resp, mensagens, limite=1500):
    bloco = ""
    for m in mensagens:
        if len(bloco) + len(m) + 2 < limite:
            bloco += f"\n\n{m}"
        else:
            resp.message(bloco.strip())
            bloco = f"{m}"
    if bloco:
        resp.message(bloco.strip())

@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.form.get('Body').strip().lower()
    sender = request.form.get('From')

    print(f"Mensagem de {sender}: {incoming_msg}")

    resp = MessagingResponse()

    if incoming_msg in ["oi", "olá", "comecar", "começar", "início", "inicio"]:
        resp.message(mensagem_inicial)
    elif incoming_msg in ["todos", "tudo", "enviar tudo", "todas"]:
        todas_formatadas = [f"{i+1}. {elogio}" for i, elogio in enumerate(elogios)]
        enviar_em_blocos(resp, todas_formatadas)
    else:
        try:
            num = int(incoming_msg)
            if 1 <= num <= len(elogios):
                resp.message(elogios[num - 1])
            else:
                resp.message("Por favor, envie um número entre 1 e 36 ou digite 'todos' para receber todos os elogios. 😉")
        except ValueError:
            resp.message("Oi! Para receber um elogio especial, envie um número entre 1 e 36 ou digite 'todos' para ver todos de uma vez. 😄")

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
