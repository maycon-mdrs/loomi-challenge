import pytest
import json
import pathlib
from datetime import datetime
from langchain_openai import ChatOpenAI
from app.core_ai.agents.supervisor_workflow import get_supervisor_workflow

# Configurações
EXAMPLES_PATH = pathlib.Path("tests/data/questions_answers_examples.json")

RESULTS_DIR = pathlib.Path("tests/results")
RESULTS_DIR.mkdir(parents=True, exist_ok=True)
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
RESULTS_FILE = RESULTS_DIR / f"results_{timestamp}.json"


def load_examples(path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_results(result):
    if RESULTS_FILE.exists():
        historico = json.loads(RESULTS_FILE.read_text(encoding="utf-8"))
    else:
        historico = []
    historico.append(result)
    RESULTS_FILE.write_text(
        json.dumps(historico, indent=2, ensure_ascii=False), encoding="utf-8"
    )


def validate_json(content):
    try:
        return json.loads(content)
    except Exception:
        pytest.fail(f"Resposta do juiz inválida: {content}")


def judge_response(judge_model, pergunta, resposta_gerada, esperada):
    prompt = f"""
    Compare a RESPOSTA GERADA com a RESPOSTA ESPERADA.

    Pergunta: {pergunta}

    RESPOSTA GERADA:
    {resposta_gerada}

    RESPOSTA ESPERADA:
    {esperada}

    Avalie se a resposta é adequada.
    Responda em JSON:
    {{
        "score": <0 a 10>,
        "veredito": "similar" ou "não similar"
    }}
    """
    result = judge_model.invoke([{"role": "user", "content": prompt}])
    return validate_json(result.content)


@pytest.mark.filterwarnings("ignore::DeprecationWarning")
@pytest.mark.filterwarnings("ignore::PendingDeprecationWarning")
@pytest.mark.filterwarnings("ignore:PydanticDeprecatedSince20")
@pytest.mark.parametrize("example", load_examples(EXAMPLES_PATH))
def test_chatbot_answers(example):
    graph = get_supervisor_workflow()
    judge_model = ChatOpenAI(model="gpt-4.1-mini", temperature=0)

    pergunta = example["pergunta"]
    esperada = example["esperada"]

    # Supervisor responde
    result = graph.invoke({"messages": [{"role": "user", "content": pergunta}]})
    resposta_gerada = result["messages"][-1].content

    # LLM julga
    avaliacao_json = judge_response(judge_model, pergunta, resposta_gerada, esperada)
    score = avaliacao_json.get("score", 0)
    veredito = avaliacao_json.get("veredito", "não similar")

    # Salva resultado
    resultado = {
        "pergunta": pergunta,
        "esperada": esperada,
        "resposta_gerada": resposta_gerada,
        "avaliacao": avaliacao_json,
    }
    save_results(resultado)

    # Assert
    assert score >= 7 and veredito == "similar", (
        f"Resposta ruim para '{pergunta}'.\n"
        f"Esperada: {esperada}\n"
        f"Gerada: {resposta_gerada}\n"
        f"Avaliação: {avaliacao_json}"
    )
