
# 💻 PintAI

PintAI é um Catálogo Inteligente de Tintas com IA. O projeto consiste em um Assistente Virtual especializado em tintas, capaz de recomendar o produto Suvinil ideal para cada pessoa, considerando seu contexto, dúvidas e preferências. Utilizando inteligência artificial, o PintAI atua como um especialista, facilitando a escolha da tinta mais adequada para cada situação.

<!--ts-->
* [📋 Requisitos](#requisitos)
* [⚙️ Setup do Projeto](#setup-do-projeto)
* [🐋 Rodar com Docker](#rodar-com-docker)
* [💻 Rodar localmente](#rodar-localmente)
* [ "Arquitetura" de solução IA](#arquitetura-de-solução-ia)
  * [🧠 Ferramentas de IA Utilizadas](#-ferramentas-de-ia-utilizadas)
  * [💬 Exemplos de Prompts Utilizados](#-exemplos-de-prompts-utilizados)
  * [🛠️ Decisões Técnicas Baseadas nas Sugestões](#%EF%B8%8F-decisões-técnicas-baseadas-nas-sugestões)
* [💬 Endpoint de Conversa](#endpoint-de-conversa)
* [Acesso](#acesso)
  * [Documentação](#documentação)
  * [Usuários de Teste](#usuários-de-teste)
* [🧪 Testes das respostas da LLM](#testes-das-respostas-da-llm)
* [📁 Estrutura de Pastas](#estrutura-de-pastas)
<!--te-->


# Requisitos
### Para usar com Docker:
- [Docker](https://www.docker.com/products/docker-desktop)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Para rodar localmente:
- [Python 3.13.5](https://www.python.org/downloads/release/python-3135/)
- [PostgreSQL](https://www.postgresql.org/download/)
- [pgvector](https://github.com/pgvector/pgvector)

# Setup do Projeto

1. Clone o repositório:
  ```bash
  git clone https://github.com/maycon-mdrs/loomi-challenge.git
  ```

2. Antes de rodar o projeto, crie um arquivo `.env` seguindo o modelo do `.env.example`. Este arquivo deve conter todas as variáveis necessárias para o funcionamento do backend e do Docker.

Principais variáveis de ambiente:

| Variável                | Descrição                                      |
|------------------------ |------------------------------------------------|
| DATABASE_USER           | Usuário do banco de dados                      |
| DATABASE_PASSWORD       | Senha do banco de dados                        |
| POSTGRES_DB             | Nome do banco de dados                         |
| DATABASE_URL            | URL de conexão do banco de dados               |
| -                       | -                                              |
| SECRET_KEY              | Chave secreta para autenticação JWT            |
| ALGORITHM               | Algoritmo JWT (ex: HS256)                      |
| -                       | -                                              |
| OPENAI_API_KEY          | Chave da API OpenAI                            |
| LANGSMITH_TRACING       | Ativa/desativa tracing do LangSmith            |
| LANGSMITH_ENDPOINT      | Endpoint do LangSmith                          |
| LANGSMITH_API_KEY       | Chave da API LangSmith                         |
| LANGCHAIN_PROJECT       | Nome do projeto LangChain                      |
| -                       | -                                              |
| MODEL_SUPERVISOR        | Modelo do agente supervisor, ex: gpt-4.1       |
| TEMPERATURE_SUPERVISOR  | Temperatura do supervisor, ex: 0               |
| MODEL_PAINTS            | Modelo do agente de tintas, ex: gpt-4.1        |
| TEMPERATURE_PAINTS      | Temperatura do agente de tintas, ex: 0         |
| MODEL_VIZUALIZER        | Modelo do agente visualizador, ex: gpt-4.1     |
| TEMPERATURE_VIZUALIZER  | Temperatura do agente visualizador, ex: 0      |

### Exemplo de uso de _DATABASE_URL_ no .env
```bash
# docker-compose
DATABASE_URL="postgresql+psycopg2://postgres/loomi?user=postgres&password={password}"

# desenvolvimento local
DATABASE_URL="postgresql+psycopg2://localhost/loomi?user=postgres&password={password}"
```


# Rodar com Docker

Para rodar o projeto com Docker, utilize o comando:
```bash
docker-compose up -d --build
# http://localhost:8080/api/v1/
# http://localhost:8080/docs
```

# Rodar localmente

### Criação do ambiente virtual
```bash
python -m venv venv
```

### Ativar o ambiente virtual
```bash
# Windows
.\venv\Scripts\activate
# Linux/macOS
source venv/bin/activate
```

### Instalar dependências
```bash
pip install -r requirements.txt
```

### Migrar o banco de dados
```bash
alembic upgrade head
```

### Iniciar aplicação
```bash
uvicorn app.main:app --reload
# http://localhost:8000/api/v1/
# http://localhost:8000/docs
```


# "Arquitetura" de solução IA
<img src="supervisor_workflow.png" alt="Supervisor Workflow" width="400"/>


### 🧠 Ferramentas de IA Utilizadas

- **OpenAI GPT (ChatGPT, Assistants API, Embeddings API)**: Utilizado para geração de respostas, engenharia de prompts, RAG e integração com agentes conversacionais.
- **DALL·E**: Geração visual opcional de ambientes pintados com a tinta recomendada.
- **LangChain**: Framework para orquestração de agentes, integração de RAG e gerenciamento de contexto conversacional.
- **LangGraph**: Implementação de agentes reativos e supervisores em grafo.
- **LangSmith**: Monitoramento e análise de aplicações com LLMs.


### 💬 Exemplos de Prompts Utilizados

- "Quero pintar meu quarto, mas prefiro algo que seja fácil de limpar e sem cheiro forte. Tem alguma sugestão?"
- "Preciso pintar a fachada da minha casa. Bate muito sol e chove bastante por aqui. Qual tinta você recomenda?"
- "Você tem alguma tinta para madeira que seja resistente ao calor?"
- "Quero pintar meu escritório com um tom de cinza moderno. Mostra como ficaria?"
- "Quero pintar minha varanda de azul claro, algo moderno e resistente ao tempo. Como ficaria?"

> Para o system prompt base do agente supervisor, encontra-se na pasta `prompts`, os demais prompts estão hardcoded nos agentes específicos, mas podem ser facilmente identificados e extraídos para um local centralizado se necessário.


### 🛠️ Decisões Técnicas Baseadas nas Sugestões
- **Arquitetura**: Separação das camadas de IA e API
- **RAG + Embeddings**: Implementação de busca inteligente na base de tintas usando embeddings e RAG
- **Agentes Multi-Ferramentas**: Uso de agentes capazes de raciocinar e decidir qual ferramenta utilizar (busca, recomendação, geração de imagem), conforme prompts e exemplos sugeridos.
- **Documentação**: Uso de Swagger
- **"Deploy"**: Docker + Docker Compose para garantir portabilidade e fácil validação do ambiente.

# Endpoint de Conversa

Aqui abordaremos um poquinho sobre o usso do endpoint de conversa, já que ele existe uma "lógica". Para interagir com o assistente, utilize o endpoint `/api/v1/chat`, que aceita requisições POST com o seguinte corpo:

```json
{
  "user_id": 123, # caso não tenha um usuário, pode ser qualquer número inteiro
  "chat_id": null,
  "prompt": "Quero pintar meu quarto, mas prefiro algo que seja fácil de limpar e sem cheiro forte. Tem alguma sugestão?"
}
```

**Fluxo de uso:**
- **Primeira mensagem:** Ao iniciar uma conversa, envie `chat_id` como `null`. O backend irá criar uma nova sessão e retornar um `chat_id` único.
- **Continuação:** Para continuar a conversa, utilize o `chat_id` retornado anteriormente no corpo da requisição. Assim, o contexto da conversa será mantido.

Exemplo de requisição inicial:
```bash
curl -X POST "http://localhost:8000/api/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 123,
    "chat_id": null,
    "prompt": "Quero pintar meu quarto, mas prefiro algo que seja fácil de limpar e sem cheiro forte. Tem alguma sugestão?"
  }'
```

Exemplo de requisição para continuar a conversa:
```bash
curl -X POST "http://localhost:8000/api/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 123,
    "chat_id": "<chat_id_retornado>",
    "prompt": "Quero pintar minha varanda de azul claro, algo moderno e resistente ao tempo. Como ficaria?"
  }'
```

O retorno segue o modelo abaixo:
```json
{
  "user_id": 123,
  "chat_id": "<chat_id_retornado>",
  "response": "Sugiro o tom Cinza Urbano da linha Suvinil Fosco Completo. O que acha?",
  "context": [ ... ]
}
```

Assim, basta guardar o `chat_id` retornado para manter o histórico e o contexto da conversa.

# Testes das respostas da LLM

Para garantir a qualidade das respostas do assistente, o projeto utiliza a seguinte abordagem: uma LLM é usada como “juiz” para avaliar automaticamente as respostas geradas pelo sistema.

O teste automatizado `tests/test_llm_quality.py` funciona assim:
- Para cada exemplo de pergunta e resposta esperada, o supervisor gera uma resposta. Os exemplos estão em `tests/data/questions_answers_examples.json`.
- Essa resposta gerada é enviada para uma LLM, junto com a resposta esperada, pedindo uma avaliação comparativa.
- A LLM retorna um veredito em formato JSON, indicando se as respostas são “similares” e atribuindo um score de 0 a 10.
- O teste só passa se o score for maior ou igual a 7 e o veredito for “similar”.

Todos os resultados dessas avaliações são salvos automaticamente em `tests/results/results_{timestamp}.json`. Esse arquivo registra cada pergunta, resposta esperada, resposta gerada e a avaliação da LLM, permitindo acompanhar a evolução da qualidade do sistema.

Exemplo de registro salvo:
```json
{
  "pergunta": "Quero pintar meu quarto, mas prefiro algo que seja fácil de limpar e sem cheiro forte. Tem alguma sugestão?",
  "esperada": "Para ambientes internos como quartos, uma boa opção é a Suvinil Toque de Seda, que possui acabamento acetinado, é lavável e tem tecnologia sem odor.",
  "resposta_gerada": "Para ambientes internos, recomendamos Suvinil Toque de Seda, que é lavável e sem cheiro forte.",
  "avaliacao": {
    "score": 9,
    "veredito": "similar"
  }
}
```

Para rodar os testes e gerar o arquivo de resultados:
```bash
pytest tests/test_llm_quality.py -p no:warnings
```

> Os testes que tendem a gerar imagens (como o agente de visualização), tendem a falhar, pois não há uma LLM para avaliar a qualidade da imagem gerada.

# Acesso

### Documentação
- [Swagger UI](http://localhost:8000/docs)

### Usuários de Teste

| Tipo de Usuário   | Email               | Senha  |
|-------------------|---------------------|--------|
| Admin             | admin@example.com   | 123    |
| Usuário Comum     | user@example.com    | 123    |

# Estrutura de Pastas
```plaintext
app/                  
 ├── core_ai/         # Lógica de IA, integração com modelos e agentes
 │    └── agents/     # Agentes especializados (ex: supervisor, paints, dalle)
 ├── database/        # Conexão, base e armazenamento vetorial do banco 
 ├── DTOs/            
 ├── exceptions/      # Definição e tratamento de exceções customizadas
 ├── models/          # Modelos das entidades do sistema
 ├── repositories/    # Repositórios para acesso e manipulação dos dados
 ├── routes/          # Rotas da API (endpoints)
 ├── services/        # Regras de negócio e serviços da aplicação
 └── utils/           # Funções utilitárias e helpers
```
