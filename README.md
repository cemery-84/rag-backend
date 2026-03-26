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

- `http://localhost:8000/docs` - Displays the Swagger documentation for the backend application
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
- `http://localhost:8000/conversations` - Provides POST and GET operations to Create and Retrieve Conversations
    - Get Conversations - Gets a list of conversations
        - Method: GET
        - Body: None
    - Create Conversation - Creates a single conversation
        - Method: POST
        - Body: Raw JSON
            - title: Title for the conversation (Defaults to "New Conversation")
- `http://localhost:8000/conversations/{conversation_id}` - Currently only DELETE operation is supported to delete a conversation
    - Method: DELETE
    - Body: None
    - {conversation_id}: The Id of the Conversation to be deleted
- `http://localhost:8000/conversations/{conversation_id}/messages` - Provides POST and GET operations to Create and Retrieve Messages within a Conversation
    - Get Messages - Gets a list of conversation messages
        - Method: GET
        - Body: None
        - {conversation_id}: The Id of the Conversation which contains the Messages to be retrieved
    - Create Message - Creates a single message in the provided conversation
        - Method: POST
        - Body: Raw JSON
            - role: Role of the message (user, assistant)
            - content: Text content of the message
        - {conversation_id}: The Id of the Conversation in which to create the Message

# Docker commands

- `docker build -t fastapi-app .` - Builds the Docker image locally
- `docker build --no-cache -t fastapi-app .` - Builds the Docker image locally forcing it to rebuild cleanly
- `docker run --env-file .env -p 8000:8000 fastapi-app` - Runs the Docker container locally
- `docker ps` - Lists Docker containers
- `docker exec <container-name> printenv` - Prints the list of Environment Variables for the container
    - `<container-name>` is the random Name Docker creates for the container
- Adding the Docker container to the Azure Container Registry
    - `az login` - Log into Azure CLI
    - `az acr login --name aichatappcontainer` - Log into the Azure ACR
    - `docker tag fastapi-app aichatappcontainer.azurecr.io/fastapi-app:latest` - Tag the local Docker image for ACR
    - `docker push aichatappcontainer.azurecr.io/fastapi-app:latest` - Push the image to ACR

# Steps to Deploy

1. `docker build --no-cache -t fastapi-app .` - Builds the Docker image locally forcing it to rebuild cleanly
1. `docker tag fastapi-app aichatappcontainer.azurecr.io/fastapi-app:latest` - Tag the local Docker image for ACR
1. `az login` - Log into Azure CLI if not already logged in
1. `az acr login --name aichatappcontainer` - Log into the Azure ACR
1. `docker push aichatappcontainer.azurecr.io/fastapi-app:latest` - Push the image to ACR
1. Create a revision of the `fastapi-app-container` (powershell)
    ```powershell
    az containerapp update `
        --name fastapi-app-container `
        --resource-group caseyemerydev-rg `
        --image aichatappcontainer.azurecr.io/fastapi-app:latest
    ```
1. Verify new revision is created
    - Go to portal.azure.com
    - Container Apps > fastapi-app-container
    - Application > Revisions and replicas
    - Ensure
        - The revision number has changed
        - It is Active
        - Running status: Running

## Alternative Deploy (easiest)

1. Update `deploy.ps1` script as necessary and save
1. Run `.\deploy.ps1`

# Kubernetes

- `az aks get-credentials --resource-group caseyemerydev-rg --name ai-chat-app-aks-cluster` - Pull AKS Credentials into the local Kubeconfig
- `kubectl get nodes` - Verify the connection
- `kubectl cluster-info` - Check cluster info
