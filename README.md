# Christopher

Christopher is a modular multi-agent AI assistant using LangChain, LangGraph, and Ollama.

## Features

✅ Modular agents with auto-discovery  
✅ LangChain-powered LLM integration (ChatGPT, Claude)  
✅ CLI + API interfaces  
✅ LangGraph orchestration  
✅ Dockerized + devcontainer ready

---

## Development Setup

### 🏗 Option 1: Using Virtualenv (Recommended)

1️⃣ **Clone the repo**

```bash
git clone https://github.com/your-org/christopher.git
cd christopher
```

2️⃣ **Create a virtual environment**

```bash
python3 -m venv .venv
```

3️⃣ **Activate the virtual environment**

- On macOS/Linux:
  ```bash
  source .venv/bin/activate
  ```
- On Windows:
  ```bash
  .venv\Scripts\activate
  ```

4️⃣ **Install dependencies**

```bash
make install
```

5️⃣ **Set up pre-commit hooks**

```bash
make precommit-install
```

---

### 🏗 Option 2: Using Devcontainer (VSCode Recommended)

- Open the folder in VSCode
- Click **"Reopen in Container"**
- The devcontainer will automatically install dependencies and set up the environment

---

## Running the App

### Run with Docker Compose

```bash
make docker-run
```

### Run CLI

```bash
docker exec -it christopher python cli/cli.py
```

### Run API Server

Visit: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## Testing

```bash
make test
```

## Linting + Formatting

```bash
make lint
make format
```

---

## Environment Setup

1️⃣ Copy the `.env` example file:

```bash
cp .env.example .env
```

2️⃣ Fill in the required API keys and service URLs.

---

## GitHub Actions

All pull requests and merges to main will automatically run:

✅ Tests  
✅ Lint checks

---

## Docker Compose

Includes:
- **christopher** app
- **ollama** service (for local LLM backend)

---

## Environment Variables

The system uses:

- `OPENAI_API_KEY`
- `ANTHROPIC_API_KEY`
- `OLLAMA_BASE_URL`
- `OLLAMA_MODEL`

These should be set in a `.env` file or passed into the environment.

## Devpod

make sure that the .venv directory isn't there
```
make clean-venv
```

Then run:

```
devpod up --id chris-dev --provider kubernetes --ide cursor .
```
---

## Kubernetes

```
helm repo add otwld https://helm.otwld.com/
helm repo update
helm install ollama otwld/ollama --namespace ollama --create-namespace --values values.yaml
```

```
export POD_NAME=$(kubectl get pods --namespace ollama -l "app.kubernetes.io/name=ollama,app.kubernetes.io/instance=ollama" -o jsonpath="{.items[0].metadata.name}")
export CONTAINER_PORT=$(kubectl get pod --namespace ollama $POD_NAME -o jsonpath="{.spec.containers[0].ports[0].containerPort}")
echo "Visit http://127.0.0.1:8080 to use your application"
kubectl --namespace ollama port-forward $POD_NAME 8080:$CONTAINER_PORT
```

## Contributing

✅ Please make sure to activate your virtualenv and install pre-commit hooks before committing changes.  
✅ Run `make lint` and `make test` to validate your changes.
