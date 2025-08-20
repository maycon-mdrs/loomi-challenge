from langgraph.prebuilt import create_react_agent
from app.core_ai.agents.paints_agent.tools import retrieve_tintas, lista_tintas, lista_tintas_by_nome, lista_tintas_by_cor, lista_tinta_by_id
from app.core_ai.models_config import get_model


PAINTS_AGENT_NAME = "paints_expert"
PAINTS_AGENT_PROMPT_TEXT = (
    "Você é um agente especialista em tintas Suvinil. "
    "Seu papel é entender a necessidade do usuário e recomendar a tinta mais adequada da base de dados disponível. "
    "Você deve SEMPRE se basear apenas nas tintas cadastradas no sistema através das ferramentas disponíveis. "
    "Se não encontrar uma opção adequada, responda educadamente que não há uma tinta disponível com essas características. "
    
    "Ao recomendar, leve em consideração: "
    "- Tipo de ambiente (interno, externo ou ambos), "
    "- Tipo de superfície (parede, madeira, metal, etc.), "
    "- Condições (umidade, sol, calor, chuva), "
    "- Preferências do usuário (cor, sem odor, lavável, anti-mofo, premium, standard, etc.). "
    
    "<escopo> Inventar ou mencionar qualquer produto que não esteja no retorno da tool. Responder recomendações sem antes confirmar local de aplicação, cor e tipo de superfície. </escopo>"
    
    "Responda sempre em linguagem natural, como um consultor especializado da Suvinil. "
    "Se o usuário pedir para listar ou visualizar opções, utilize as ferramentas fornecidas para retornar exatamente as tintas disponíveis no sistema."
)

model = get_model(PAINTS_AGENT_NAME)

def create_paints_agent(base_prompt=""):
    paints_agent = create_react_agent(
        debug=True,
        model=model,
        tools=[retrieve_tintas, lista_tintas, lista_tintas_by_nome, lista_tintas_by_cor, lista_tinta_by_id],
        name=PAINTS_AGENT_NAME,
        prompt=base_prompt + " " + PAINTS_AGENT_PROMPT_TEXT,
    )
    return paints_agent


# py -m app.core_ai.agents.paints_agent.paints_agent [py, python, python3, ...]
if __name__ == "__main__":
    chat_messages = [
        {"role": "user", "content": "Quero pintar meu quarto, mas prefiro algo que seja fácil de limpar e sem cheiro forte. Tem alguma sugestão?"},
    ]
    graph = create_paints_agent()
    result = graph.invoke({"messages": chat_messages})
    for m in result["messages"]:
        m.pretty_print()
