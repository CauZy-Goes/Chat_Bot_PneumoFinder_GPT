import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

elogios = [
    "🌟 Olá Dona Pamela! 🌟\n\n"
    "❤️ Cauã, seu Bê, está me testando e precisa da sua ajuda pra isso!\n\n"
    "É bem simples: mande qualquer mensagem aleatória aqui — pode ser um 'oi', um 'p', um 'sou linda e mediciner 😎'… tanto faz!\n\n"
    "Cada mensagem sua vai ajudar ele a testar o bot (e, claro, receber um elogio cheio de carinho 💌).\n\n"
    "Então bora se divertir! 😄✨",

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
    "Ufa, acabaram meus elogios por hoje 😅💌\n\nMas ó... você merece muito mais do que 15 frases bonitas. Você merece o mundo, BatGirl! 🌍❤️"
]

contador = 0  # global

@app.route("/webhook", methods=["POST"])
def webhook():
    global contador  # usamos a global para atualizar

    incoming_msg = request.form.get('Body')
    sender = request.form.get('From')

    print(f"Mensagem de {sender}: {incoming_msg}")

    resp = MessagingResponse()
    msg = resp.message()

    # Pega o elogio correspondente ao contador
    elogio = elogios[contador % len(elogios)]
    msg.body(elogio)

    print(f"Mensagem de enviada: {elogio}")

    contador += 1  # incrementa para a próxima vez

    return str(resp)


if __name__ == "__main__":
    app.run(debug=True)
