from langgraph.prebuilt import create_react_agent
from app.core_ai.models_config import get_model
from app.core_ai.agents.dalle_agent.tools import dalle_tool


DALLE_AGENT_NAME = "visualizer_expert"
DALLE_AGENT_PROMPT_TEXT = (
    "Você é um agente especializado em gerar imagens de ambientes pintados com tintas Suvinil. "
    "Receba um prompt do usuário descrevendo o ambiente, cor, acabamento ou qualquer detalhe relevante, "
    "e gere uma imagem correspondente usando o modelo DALL·E. "
    "Retorne EXCLUSIVAMENTE a URL da imagem gerada, sem markdown, sem explicação, sem texto adicional. "
    "Se não for possível gerar a imagem, responda apenas: 'Não foi possível gerar a imagem.'"
)


def create_dalle_agent(base_prompt=""):
    model = get_model(DALLE_AGENT_NAME)
    dalle_agent = create_react_agent(
        debug=True,
        model=model,
        tools=[dalle_tool],
        name=DALLE_AGENT_NAME,
        prompt=base_prompt + " " + DALLE_AGENT_PROMPT_TEXT,
    )
    return dalle_agent


# py -m app.core_ai.agents.dalle_agent.dalle_agent
if __name__ == "__main__":
    chat_messages = [
        {
            "role": "user",
            "content": "Simule um quarto pintado de azul claro, com acabamento acetinado e decoração minimalista.",
        },
    ]
    graph = create_dalle_agent()
    result = graph.invoke({"messages": chat_messages})
    for m in result["messages"]:
        print(m)
