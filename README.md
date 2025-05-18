
# WhatsApp Bots: PneumoFinder & TaskList Assistant 🤖📱

Este projeto contém **dois chatbots inteligentes integrados ao WhatsApp via Twilio** que se comunicam com APIs distintas:

- **PneumoFinder Bot**: envia uma imagem de pulmão para a API [PneumoFinder](https://github.com/CauZy-Goes/PneumoFinder) e responde o diagnóstico.
- **TaskList Assistant Bot**: utiliza o ChatGPT para interpretar comandos de texto e manipular a API de tarefas [TaskList-Spring](https://github.com/CauZy-Goes/TaskList-Spring).

---

## 🤖🫁 Bot #1: PneumoFinder

- Recebe **imagem de pulmão via WhatsApp**
- Envia para a API do [PneumoFinder](https://github.com/CauZy-Goes/PneumoFinder)
- Retorna o diagnóstico com base no modelo treinado com CNN

**Tecnologias utilizadas no bot:**
- Python
- Flask
- Twilio API (WhatsApp)
- Ngrok

**Fluxo resumido:**
1. Usuário envia uma **imagem de raio-x do pulmão**
2. Bot chama a API PneumoFinder
3. Responde o diagnóstico: `"Pulmão saudável"` ou `"Suspeita de pneumonia"`

---

## 🤖✅ Bot #2: TaskList Assistant (com ChatGPT)

- Interpreta mensagens do usuário com **OpenAI GPT**
- Executa ações na API de tarefas: `listar`, `adicionar`, `remover`
- Envia para a API do [TaskList-Spring](https://github.com/CauZy-Goes/TaskList-Spring)
- Mantém contexto de conversa por usuário (histórico limitado a 20 mensagens)

**Tecnologias utilizadas no bot:**
- Python
- Flask
- OpenAI GPT-4
- Twilio API (WhatsApp)
- Ngrok
- API TaskList-Spring

**Exemplos de comandos que o usuário pode enviar:**
- "Adicione uma tarefa para estudar Spring Security"
- "Remova a tarefa 3"
- "Quais são minhas tarefas?"
- Ou até mesmo: "Você pode me lembrar de beber água?" (resposta natural via GPT)

---

## 🌐 APIs Integradas

| Bot | API                | Repositório                                          |
|-----|--------------------|-------------------------------------------------------|
| 🫁 PneumoFinder | Classificação de Imagens | [PneumoFinder](https://github.com/CauZy-Goes/PneumoFinder) |
| ✅ TaskList Assistant | Gerenciamento de Tarefas | [TaskList-Spring](https://github.com/CauZy-Goes/TaskList-Spring) |

---

## 📸 Prints de exemplo

### 🫁 PneumoFinder
Bot treinado para classificar imagens de pulmões (com ou sem pneumonia) via WhatsApp.

![PneumoFinder 1](https://github.com/CauZy-Goes/Meu_Chat_Bot_Twillio/blob/main/imgs_projeto/pneumofinder1.png)
![PneumoFinder 2](https://github.com/CauZy-Goes/Meu_Chat_Bot_Twillio/blob/main/imgs_projeto/pneumofinder2.png)

---

### ✅ TaskList Bot
Bot que permite gerenciar tarefas via WhatsApp (adicionar, listar e excluir tarefas).

![TaskList 1](https://github.com/CauZy-Goes/Meu_Chat_Bot_Twillio/blob/main/imgs_projeto/tasklist1.png)
![TaskList 2](https://github.com/CauZy-Goes/Meu_Chat_Bot_Twillio/blob/main/imgs_projeto/tasklist2.png)

---

## 🧪 Testando

Você pode expor o webhook local com ferramentas como **ngrok**:

```bash
ngrok http 5000
```

Depois configure o Webhook do número do Twilio no painel com a URL `https://<seu_ngrok>.ngrok.io/webhook`.

---

## 📦 requirements.txt

As dependências do projeto estão listadas no arquivo [`requirements.txt`](./requirements.txt). Principais pacotes:

- Flask
- Twilio
- OpenAI SDK
- python-dotenv
- requests

---

## 🚀 Como Executar

### 1. Clone o Repositório

```bash
git clone https://github.com/CauZy-Goes/whatsapp-gpt-bots.git
cd whatsapp-gpt-bots
```

### 2. Crie um ambiente virtual e ative-o

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto com o seguinte conteúdo:

```
TWILIO_ACCOUNT_SID=seu_sid_twilio
TWILIO_AUTH_TOKEN=seu_token_twilio
TWILIO_NUMBER=whatsapp:+5511999999999
OPENAI_API_KEY=sua_chave_openai
```


---

## 📄 Licença

Este projeto está licenciado sob os termos da licença MIT.  
Consulte o arquivo [LICENSE](https://github.com/CauZy-Goes/Meu_Chat_Bot_Twillio/blob/main/LICENSE) para mais informações.

---
## 👤 Autor

Desenvolvido por [Cauã Farias (CauZy-Goes)](https://github.com/CauZy-Goes)  
📧 cauafariasdev@gmail.com  
💼 [LinkedIn](https://www.linkedin.com/in/cauã-farias)

