# rag-backend

Simple AI Chat App RAG Backend written using Python and used Ollama for the LLM

# Setup

- Ensure you have Python 3.11 or greater installed on your computer.
- Open a cmd prompt int eh project folder
- Run `python -m venv .venv` to setup the environment folder
- Run `.\venv\Scripts\activate` to activate the environment
- Run `python -m pip install --upgrade pip` to upgrade the pip installer (Optional)
- Run `pip install -r requirements.txt` to install the required python libraries

# Running the project

- Open cmd prompt or powershell
- Switch to the project directory
- Run `.\venv\Scripts\activate` to activate teh enviroment if not already active
- Run `.\venv\Scripts\uvicorn app.main:app --reload` to run the RAG Backend app as a web application
- Open a browser and go to `http://localhost:8000/docs` to verify the app is running

# Routes

- `http://localhost:8000/ingest` - Used to ingest documents
    - Method: POST
    - Content-Type: multipart/form-data
    - Body
        - file: pdf file to ingest
- `http://localhost:8000/query` - Given a user query, embed it and search the Chroma collection. Returns the raw Chroma query result.
    - Method: POST
    - Body: Raw JSON
        - query: string - Text that users is querying about
        - n_results: number - The number of results to return
- `http://localhost:8000/chat` - Accepts a user query, retrieves relevant chunks from Chroma, and generates a response using the local Ollama model. Returns the results as JSON data
    - Method: POST
    - Body: Raw JSON
        - message: string - Text that users is querying about
        - n_results: number - The number of results to return
- `http://localhost:8000/chat/stream` - Accepts a user query, retrieves relevant chunks from Chroma, and generates a streaming response using the local Ollama model. Uses Server-Sent Events (SSE) for streaming.
    - Method: POST
    - Body: Raw JSON
        - message: string - Text that users is querying about
        - n_results: number - The number of results to return
