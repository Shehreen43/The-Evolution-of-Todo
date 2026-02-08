# Evolution of Todo - AI Backend

This is the FastAPI backend for the **Evolution of Todo** application. It provides a robust API for task management with integrated AI chatbot capabilities for natural language task interaction.

## 🚀 Features

- **FastAPI Core**: High-performance asynchronous API.
- **AI Chatbot**: Intelligent task management via Groq or OpenRouter (Llama 3.1 & fallback models).
- **PostgreSQL Database**: Persistent storage via Neon DB with SQLAlchemy ORM.
- **Modern Auth**: Structured authentication support with `Better-Auth`.
- **Database Migrations**: Managed via Alembic.
- **Dockerized**: Ready for deployment on Hugging Face Spaces or any Docker-compatible hosting.

## 🛠️ Tech Stack

- **Framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **Database**: [PostgreSQL (Neon)](https://neon.tech/)
- **ORM**: [SQLAlchemy](https://www.sqlalchemy.org/)
- **AI Integration**: [Groq](https://groq.com/) / [OpenRouter](https://openrouter.ai/)
- **Deployment**: [Hugging Face Spaces](https://huggingface.co/spaces) (Docker)

## 📦 Deployment on Hugging Face

To deploy this backend on Hugging Face Spaces:

1.  Create a new **Docker Space**.
2.  Upload the contents of the `backend/` directory.
3.  Go to the **Settings** tab of your Space.
4.  Add the following **Variables and Secrets**:
    - `DATABASE_URL`: Your Neon DB connection string.
    - `BETTER_AUTH_SECRET`: A long random string for auth security.
    - `GROQ_API_KEY`: Your Groq API key.
    - `FRONTEND_URL`: The URL of your deployed frontend.
    - `CORS_ORIGINS`: Comma-separated list of allowed origins.
    - `ENVIRONMENT`: Set to `production`.

## 💻 Local Setup

1.  **Clone the repository**:
    ```bash
    git clone <your-repo-url>
    cd backend
    ```

2.  **Create a virtual environment**:
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment**:
    - Copy `.env.example` to `.env`.
    - Fill in your local/development credentials.

5.  **Run the application**:
    ```bash
    uvicorn app.main:app --reload
    ```

## 📖 API Documentation

Once the server is running, you can access the interactive Swagger documentation at:
- `http://localhost:8000/docs`
