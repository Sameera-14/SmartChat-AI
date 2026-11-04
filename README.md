# SmartChat AI – Your Friendly AI Assistant

SmartChat AI is an intelligent chatbot powered by a Large Language Model (LLM) API. It provides interactive conversations while maintaining context from previous messages.

The chatbot is designed to deliver a friendly user experience with multi-turn conversation memory and context window management.

## Features

- **AI-Powered Conversations:** Generates intelligent responses using the Groq API.
- **Multi-Turn Conversation:** Remembers previous messages within a conversation.
- **Context Window Management:** Retains the most recent 12 messages to manage conversation history.
- **Personalized Responses:** Uses a custom system prompt to define the chatbot's personality.
- **User-Friendly Interface:** Simple and interactive chat interface.
- **New Chat Option:** Allows users to start a fresh conversation.
- **Error Handling:** Handles API failures and displays appropriate error messages.
- **Secure API Configuration:** Stores API credentials in environment variables.

## 🛠️ Technologies Used

- **Python** – Backend development
- **Flask** – Web framework
- **Groq API** – Large Language Model integration
- **HTML** – Frontend structure
- **CSS** – User interface styling
- **JavaScript** – Frontend interactions
- **Python-dotenv** – Environment variable management

## Project Structure


SmartChat-AI/
│
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
│
├── static/
│   ├── script.js
│   └── style.css
│
└── templates/
    └── index.html


## ⚙️ Installation and Setup

### 1. Clone the repository

git clone https://github.com/Sameera-14/SmartChat-AI.git

### 2. Navigate to the project directory

cd SmartChat-AI

### 3. Create a virtual environment

python -m venv .venv

### 4. Activate the virtual environment

For Windows:
.venv\Scripts\activate

### 5. Install dependencies

pip install -r requirements.txt


### 6. Configure the API key

Create a .env file in the project directory.

Add the following:


GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=groq/gpt-oss-20b

Get your API key from [Groq Console](https://console.groq.com/keys).

**Important:** Never upload your `.env` file or expose your API key on GitHub.

### 7. Run the application

```bash
python app.py
```

Open your browser and visit the local URL displayed in the terminal.

## 🧠 How It Works

1. The user enters a message through the chat interface.
2. The frontend sends the message to the Flask backend.
3. The backend maintains conversation history.
4. Recent messages are passed to the Groq LLM API along with a custom system prompt.
5. The AI generates a response.
6. The response is displayed in the chat interface.
7. Previous conversation context is maintained for subsequent messages.

## 🔒 Security

- API keys are stored in environment variables.
- `.env` is excluded using `.gitignore`.
- `.env.example` provides a sample configuration without exposing secrets.

## 🎯 Project Objective

The main objective of SmartChat AI is to build an intelligent chatbot that can maintain meaningful multi-turn conversations using a real LLM API and effective context window management.

## 👩‍💻 Author

**Sameera**

GitHub: https://github.com/Sameera-14/SmartChat-AI

---

⭐ If you find this project interesting, consider giving it a star!
