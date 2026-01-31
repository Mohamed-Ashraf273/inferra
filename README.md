# 🤖 Inferra

**Inferra** is an intelligent AI chatbot powered by **LangChain** and **Groq**, designed to integrate with multiple AI models and tools. It provides a conversational interface where users ca## 🛠️ Technology Stack

- **Backend**: FastAPI, WebSocket, Python 3.12
- **Frontend**: HTML, CSS, JavaScript (Vanilla)
- **AI Framework**: LangChain (ReAct Agent Pattern)
- **LLM Provider**: Groq (llama-3.1-8b-instant)
- **Agent Tools**: 
  - Sound Classifier (50+ sound categories)
  - Extensible tool integration system
- **Session Management**: Multi-session support with independent conversation contexts
- **Containerization**: Dockerct with various AI capabilities through natural language.

We are a group of students from the **Faculty of Engineering, Cairo University**, building a versatile chatbot that can access different AI models and tools to assist users with a wide range of tasks.

---

## Features

- 🤖 **Intelligent AI Agent** - Powered by LangChain's ReAct pattern with reasoning and action capabilities
- 🔗 **Multi-Model Integration** - Connect and interact with multiple AI models and tools
- 💬 **Real-time Chat** - WebSocket-based streaming for instant responses
- 🧠 **Conversational Memory** - Maintains context throughout the conversation
- 🎵 **Sound Classification** - Upload audio files and get intelligent sound analysis and classification
---

## 🏗️ How It Works

Inferra uses a **LangChain-powered agent** that can:
- Understand natural language queries
- Access multiple AI models and tools
- Provide intelligent responses with reasoning
- Maintain conversation context across multiple messages

The agent follows the **ReAct pattern** (Reasoning + Acting), allowing it to think through problems and take actions using various tools and models at its disposal.

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.9+**
- **Docker** (optional, for containerized deployment)
- **Groq API Key** ([Get one here](https://console.groq.com/))

---

## 📦 Running with Docker (Recommended)

### 1. Clone the repository

```bash
git clone https://github.com/Mohamed-Ashraf273/inferra.git
cd inferra
```

### 2. Build the Docker image

```bash
docker build -t inferra:latest .
```

### 3. Run the container

```bash
docker run -d \
  --name inferra-app \
  -p 8000:8000 \
  -p 3000:3000 \
  -e GROK_API_KEY=your_groq_api_key_here \
  inferra:latest
```

### 4. Access the application

- **Chat UI**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

### 5. View logs

```bash
docker logs -f inferra-app
```

### 6. Stop the application

```bash
docker stop inferra-app
docker rm inferra-app
```

---

## 💻 Running Locally (Without Docker)

### 1. Clone the repository

```bash
git clone https://github.com/Mohamed-Ashraf273/inferra.git
cd inferra
```

### 2. Create a virtual environment

```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

### 3. Set environment variables

Create a `.env` file in the root directory:

```bash
GROK_API_KEY=your_groq_api_key_here
```

Or export directly:

```bash
export GROK_API_KEY=your_groq_api_key_here
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```


### 5. Start the backend server

```bash
python -m uvicorn app.backend.main:app --reload --port 8000
```

### 6. Start the frontend server (in a new terminal)

```bash
cd app/frontend
python -m http.server 3000
```

### 7. Access the application

- **Chat UI**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

---

### API Endpoints

- `GET /` - Health check
- `POST /sessions` - Create a new chat session
- `GET /sessions` - List all chat sessions
- `DELETE /sessions/{session_id}` - Delete a specific session
- `DELETE /sessions` - Delete all sessions
- `POST /sessions/{session_id}/upload-audio` - Upload audio file to a session
- `WebSocket /ws/chat/{session_id}` - WebSocket endpoint for real-time chat

---

## Contributing

We welcome contributions from everyone! Here's how you can get started:

### How to Contribute

1. **Fork the repository** and create your branch from `main`.
2. **Clone your fork** and set up the development environment:
    ```bash
    git clone https://github.com/your-username/inferra.git
    cd inferra
    pip install -r requirements.txt
    ```
3. **Create a new branch** for your feature or bugfix:
    ```bash
    git checkout -b my-feature
    ```
4. **Make your changes**, following these guidelines:
    - Add new **AI models** or **tools** in `inferra/src/` to extend the chatbot's capabilities.
    - If you create **new layers** or utilities, add them under `inferra/src/layers/`.
    - To integrate new AI services, update the agent configuration in `inferra/src/core/`.
    - Keep the codebase clean and well-documented.

5. **Run pre-commit checks before committing:**
    ```bash
    pre-commit run --all-files --hook-stage manual
    ```

6. **Commit and push** your changes:
    ```bash
    git add .
    git commit -m "Describe your changes"
    git push origin my-feature
    ```

7. **Open a Pull Request** on GitHub and describe your changes clearly.

---

## Technology Stack

- **Backend**: FastAPI, WebSocket, Python 3.12
- **Frontend**: HTML, CSS, JavaScript (Vanilla)
- **AI Framework**: LangChain, LangGraph
- **LLM Provider**: Groq (llama-3.1-8b-instant)
- **ML Frameworks**: PyTorch, TensorFlow
- **Containerization**: Docker

---

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GROK_API_KEY` | Your Groq API key for LLM access | Yes |
| `API_HOST` | Backend host (default: 0.0.0.0) | No |
| `API_PORT` | Backend port (default: 8000) | No |

---

## Troubleshooting

### Backend won't start

- Make sure you have set the `GROK_API_KEY` environment variable
- Check if port 8000 is already in use: `lsof -i :8000`
- Verify all dependencies are installed: `pip install -r requirements.txt`

### Frontend can't connect to backend

- Ensure the backend is running on port 8000
- Check the WebSocket URL in `app/frontend/script.js` (should be `ws://localhost:8000/ws/chat`)
- Look at browser console for connection errors (F12)

### Docker container issues

- Check logs: `docker logs inferra-app`
- Verify ports are not in use: `docker ps`
- Rebuild image: `docker build -t inferra:latest . --no-cache`

---

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

---

## Team

Created with ❤️ by students from the **Faculty of Engineering, Cairo University**.

---

## Star History

If you find this project useful, please consider giving it a star! ⭐

---

## Contact

For questions or support:
- Open an issue on [GitHub](https://github.com/Mohamed-Ashraf273/inferra/issues)
- Join our [Discussions](https://github.com/Mohamed-Ashraf273/inferra/discussions)

---

**Happy coding! Join the Inferra community and help make AI accessible for everyone!** 🚀
