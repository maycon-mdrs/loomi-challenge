import os
from langgraph_supervisor import create_supervisor
from app.core_ai.agents.dalle_agent.dalle_agent import create_dalle_agent
from app.core_ai.agents.paints_agent.paints_agent import create_paints_agent
from app.core_ai.models_config import ModelConfig
from app.core_ai.agents.base_prompt import PROMPT_BASE_TEXT
from app.utils.utils import read_system_prompt_from_file

file_path = os.path.abspath("./prompt/system_prompt.txt")
system_prompt_content = read_system_prompt_from_file(file_path)

model_config = ModelConfig()
model = model_config.get_model("supervisor")

base_prompt = PROMPT_BASE_TEXT.format(
    organization_name="Loomi Digital", 
    organization_acronym="Loomi"
)

_paints_agent = create_paints_agent(base_prompt=base_prompt)
_dalle_agent = create_dalle_agent(base_prompt=base_prompt)

_SUPERVISOR_WORKFLOW = create_supervisor(
    agents=[_paints_agent, _dalle_agent],
    model=model,
    prompt=(
        system_prompt_content
        + "\n\nVocê é um supervisor que gerencia agentes especializados em tintas e recomendações de pintura. "
        "Para questões relacionadas à escolha de tintas (acabamento, ambiente, tipo de superfície, cor, linha, resistência), utilize exclusivamente o agente 'paints_expert'. "
        "Se o usuário solicitar simulação visual da tinta aplicada em um ambiente, encaminhe a solicitação para o agente 'visualizer_expert'. Retorne sempre a resposta do agente especializado, sem adicionar informações extras. "
        "Sempre forneça uma resposta clara, natural e útil para o usuário, incluindo integralmente a resposta recebida do agente especializado na sua resposta final."
    ),
).compile()


def get_supervisor_workflow():
    return _SUPERVISOR_WORKFLOW


# py -m app.core_ai.agents.supervisor_workflow [py, python, python3, ...]
if __name__ == "__main__":
    chat_messages = [
        {"role": "user", "content": "Oi, quem é você?"},
    ]
    graph = get_supervisor_workflow()
    result = graph.invoke({"messages": chat_messages})
    for m in result['messages']:
        m.pretty_print()
