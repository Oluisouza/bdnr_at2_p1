# Chat em Tempo Real com FastAPI, MongoDB e WebSockets (Refatorado)

Este é um projeto de chat em tempo real refatorado para seguir boas práticas de organização de código, modularidade e manutenibilidade.

## Estrutura do Projeto

O projeto foi organizado da seguinte forma:

- `app/main.py`: Ponto de entrada da aplicação FastAPI.
- `app/config.py`: Carrega e gerencia as configurações do ambiente.
- `app/database.py`: Gerencia a conexão e a comunicação com o MongoDB.
- `app/models.py`: Define os modelos de dados (schemas) Pydantic.
- `app/ws_manager.py`: Abstrai a lógica de gerenciamento de conexões WebSocket.
- `app/routes/messages.py`: Contém as rotas da API (REST e WebSocket).
- `app/static/`: Contém o frontend (HTML, CSS, JS).

## Como Rodar o Projeto

### 1. Pré-requisitos
- Python 3.8+
- Uma conta no MongoDB Atlas (ou um servidor MongoDB local)

### 2. Clone o Repositório
```bash
git clone git@github.com:Oluisouza/bdnr_at2_p2.git
cd <nome-da-pasta>
```

### 3. Crie o Ambiente Virtual```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 4. Crie o Arquivo de Ambiente
Crie um arquivo chamado `.env` na raiz do projeto e adicione sua string de conexão do MongoDB:
```
MONGO_URL=mongodb+srv://<user>:<password>@<cluster-url>/...
MONGO_DB=chatdb
```

### 5. Instale as Dependências
```bash
pip install -r requirements.txt
```

### 6. Rode o Servidor
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

A aplicação estará disponível em `http://localhost:8000`.