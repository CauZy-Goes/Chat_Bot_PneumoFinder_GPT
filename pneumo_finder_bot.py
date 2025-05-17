import os
import requests
from requests.auth import HTTPBasicAuth
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

API_PNEUMO_URL = "http://localhost:5001/diagnosticar"
PASTA_IMAGENS = "imgs_pulmoes"
os.makedirs(PASTA_IMAGENS, exist_ok=True)

account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")

@app.route("/webhook", methods=["POST"])
def webhook():
    resp = MessagingResponse()
    num_media = int(request.form.get("NumMedia", 0))

    if num_media == 0:
        resp.message("Oi! Por favor, envie uma imagem do pulmão para eu diagnosticar se tem pneumonia.")
        return str(resp)

    media_url = request.form.get("MediaUrl0")

    try:
        image_response = requests.get(media_url, auth=HTTPBasicAuth(account_sid, auth_token))
        image_response.raise_for_status()
    except Exception:
        resp.message("Não consegui baixar a imagem, tenta enviar novamente, por favor.")
        return str(resp)

    import time
    timestamp = int(time.time())
    filename = f"{timestamp}.jpg"
    filepath = os.path.join(PASTA_IMAGENS, filename)

    with open(filepath, "wb") as f:
        f.write(image_response.content)

    try:
        with open(filepath, "rb") as f:
            files = {"imagem": f}
            api_response = requests.post(API_PNEUMO_URL, files=files)

        if api_response.status_code != 200:
            resp.message("Erro no diagnóstico. Tente novamente mais tarde.")
            return str(resp)

        resultado = api_response.json()
        classe = resultado.get("classe", "desconhecido")
        confianca = resultado.get("confianca", 0.0)

        if classe.lower() == "pneumonia":
            # mensagem = f"A análise indicou pneumonia com confiança de {confianca*100:.1f}%."
            mensagem = f"A análise do Pneumofinder indicou Pnumonia com confiança de {confianca*100:.1f}% 🚨"
        else:
            # mensagem = f"Não foi detectada pneumonia. Confiança: {confianca*100:.1f}%."
            mensagem = f"A análise do Pneumofinder não detectou a presença da pneumonia com confiança de {confianca*100:.1f}% ✅"

        print(mensagem)
        resp.message(mensagem)

    except Exception:
        resp.message("Tive um erro ao processar a imagem. Tenta novamente mais tarde, tá?")

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
