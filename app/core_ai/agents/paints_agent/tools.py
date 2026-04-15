from typing import Optional
from langchain_core.runnables import RunnableConfig

from app.database.connection import Session
from app.services.paint_retriever_rag_service import PaintRetrieverRagService
from app.services.paint_service import PaintService
from app.DTOs.paint_dtos import PaintResponse, PaintRegister
from app.exceptions.paint_exceptions import PaintAlreadyExistsException, PaintCreationException

retriever_service = PaintRetrieverRagService()

# Valores válidos para validação amigável
VALID_ENVIRONMENTS = {"INTERNO", "EXTERNO", "AMBOS"}
VALID_FINISH_TYPES = {"Acetinado", "Fosco", "Brilhante"}
VALID_LINES = {"Premium", "Standard"}


def retrieve_tintas(question: str):
    """
    Recupera informações relevantes sobre tintas com base em uma pergunta fornecida.

    Esta função utiliza o serviço de recuperação de informações (RAG) para buscar dados sobre tintas,
    auxiliando agentes a responder perguntas técnicas, comerciais ou gerais relacionadas a tintas disponíveis no sistema.
    
    Parâmetros:
    - question (str): A pergunta ou consulta sobre tintas que se deseja responder.
    """
    documents = retriever_service.retrieve_paints(question)
    return {"documents": documents, "question": question}


def lista_tintas():
    """
    Recupera uma lista de todas as tintas disponíveis no sistema.
    Retorna uma lista de dicionários contendo o ID e o nome de cada tinta. Para mais detalhes, usar a função `lista_tinta_by_id` ou `lista_tinta_by_name`.
    """
    db_session = Session()
    try:
        paint_service = PaintService(db_session)
        paints = paint_service.get_all_paints()
        return [
            PaintResponse(
                id=paint.id,
                paint_name=paint.paint_name,
                color=paint.color,
                surface_type=paint.surface_type,
                environment=paint.environment,
                finish_type=paint.finish_type,
                features=paint.features,
                line=paint.line,
            )
            for paint in paints
        ]
    finally:
        db_session.close()


def lista_tintas_by_nome(nome_tinta: str):
    """
    Recupera uma lista de tintas com base no nome fornecido.

    Parâmetros:
    - nome_tinta (str): Nome da tinta que se deseja consultar. Pode ser obtido a partir da função `lista_tintas`.
    """
    db_session = Session()
    try:
        paint_service = PaintService(db_session)
        paints = paint_service.get_paints_by_name(name=nome_tinta)
        return [
            PaintResponse(
                id=paint.id,
                paint_name=paint.paint_name,
                color=paint.color,
                surface_type=paint.surface_type,
                environment=paint.environment,
                finish_type=paint.finish_type,
                features=paint.features,
                line=paint.line,
            )
            for paint in paints
        ]
    finally:
        db_session.close()


def lista_tintas_by_cor(cor_tinta: str):
    """
    Recupera uma lista de tintas com base na cor fornecida.

    Parâmetros:
    - cor_tinta (str): Cor da tinta que se deseja consultar. Pode ser obtida a partir da função `lista_tintas`.
    """
    db_session = Session()
    try:
        paint_service = PaintService(db_session)
        paints = paint_service.get_paints_by_color(color=cor_tinta)
        return [
            PaintResponse(
                id=paint.id,
                paint_name=paint.paint_name,
                color=paint.color,
                surface_type=paint.surface_type,
                environment=paint.environment,
                finish_type=paint.finish_type,
                features=paint.features,
                line=paint.line,
            )
            for paint in paints
        ]
    finally:
        db_session.close()


def lista_tinta_by_id(id: int):
    """
    Recupera detalhes de uma tinta específica com base no ID fornecido.

    Parâmetros:
    - id (int): Identificador único da tinta que se deseja consultar. Pode ser obtido a partir da função `lista_tintas`.
    """
    db_session = Session()
    try:
        paint_service = PaintService(db_session)
        paint = paint_service.get_paint_by_id(paint_id=id)
        return PaintResponse(
            id=paint.id,
            paint_name=paint.paint_name,
            color=paint.color,
            surface_type=paint.surface_type,
            environment=paint.environment,
            finish_type=paint.finish_type,
            features=paint.features,
            line=paint.line,
        )
    finally:
        db_session.close()


def criar_tinta(
    paint_name: str,
    color: str,
    surface_type: str,
    environment: str,
    finish_type: str,
    features: Optional[str] = None,
    line: Optional[str] = None,
    *,
    config: RunnableConfig
):
    """
    Cria uma nova tinta no sistema.
    
    IMPORTANTE: Antes de chamar esta função, o agente DEVE:
    1. Coletar TODOS os campos obrigatórios com o usuário
    2. Pedir confirmação explícita do usuário antes de criar
    
    Parâmetros:
    - paint_name (str): Nome da tinta (ex: "Suvinil Toque de Seda")
    - color (str): Cor da tinta (ex: "Branco Neve", "Azul Sereno")
    - surface_type (str): Tipo de superfície (ex: "Alvenaria", "Madeira", "Ferro")
    - environment (str): Ambiente de aplicação. DEVE ser um dos valores: "INTERNO", "EXTERNO" ou "AMBOS"
    - finish_type (str): Tipo de acabamento. DEVE ser um dos valores: "Acetinado", "Fosco" ou "Brilhante"
    - features (str, opcional): Características especiais (ex: "Lavável, Anti-mofo, Sem odor")
    - line (str, opcional): Linha do produto. Se fornecido, DEVE ser "Premium" ou "Standard"
    """
    # Verificar se o usuário é administrador
    configurable = config.get("configurable", {})
    is_admin = configurable.get("is_admin", False)
    
    if not is_admin:
        return {"error": "Apenas administradores podem criar novas tintas. Você não tem permissão para esta operação."}
    
    # Validação amigável do campo environment
    if environment not in VALID_ENVIRONMENTS:
        return {
            "error": f"Valor inválido para 'environment': '{environment}'. "
                     f"Os valores permitidos são: {', '.join(VALID_ENVIRONMENTS)}"
        }
    
    # Validação amigável do campo finish_type
    if finish_type not in VALID_FINISH_TYPES:
        return {
            "error": f"Valor inválido para 'finish_type': '{finish_type}'. "
                     f"Os valores permitidos são: {', '.join(VALID_FINISH_TYPES)}"
        }
    
    # Validação amigável do campo line (se fornecido)
    if line is not None and line not in VALID_LINES:
        return {
            "error": f"Valor inválido para 'line': '{line}'. "
                     f"Os valores permitidos são: {', '.join(VALID_LINES)}"
        }
    
    db_session = Session()
    try:
        paint_service = PaintService(db_session)
        
        paint_data = PaintRegister(
            paint_name=paint_name,
            color=color,
            surface_type=surface_type,
            environment=environment,
            finish_type=finish_type,
            features=features,
            line=line,
        )
        
        created_paint = paint_service.create_paint(paint_data)
        
        return {
            "success": True,
            "message": f"Tinta '{paint_name}' na cor '{color}' criada com sucesso!",
            "paint": PaintResponse(
                id=created_paint.id,
                paint_name=created_paint.paint_name,
                color=created_paint.color,
                surface_type=created_paint.surface_type,
                environment=created_paint.environment.value if hasattr(created_paint.environment, 'value') else created_paint.environment,
                finish_type=created_paint.finish_type,
                features=created_paint.features,
                line=created_paint.line,
            )
        }
    except PaintAlreadyExistsException:
        return {"error": f"Já existe uma tinta com o nome '{paint_name}' e cor '{color}' cadastrada no sistema."}
    except PaintCreationException:
        return {"error": "Ocorreu um erro ao criar a tinta. Por favor, verifique os dados e tente novamente."}
    except Exception as e:
        return {"error": f"Erro inesperado ao criar a tinta: {str(e)}"}
    finally:
        db_session.close()


# py -m app.core_ai.agents.paints_agent.tools [py, python, python3, ...]
if __name__ == "__main__":
    print("Recuperando informações sobre tintas com base em uma pergunta:")
    question = "Quais tintas são recomendadas para ambientes internos com alta umidade?"
    question = "tinta para madeira resistente ao calor"
    result = retrieve_tintas(question)
    print(result)

    print("\n\nLista de tintas disponíveis:")
    print(lista_tintas())

    print("\n\nDetalhes da tinta com ID 1:")
    print(lista_tinta_by_id(1))

    print("\n\nDetalhes da tinta com nome 'Suvinil Toque de Seda':")
    print(lista_tintas_by_nome("Suvinil toque de seda"))
    
    print("\n\nDetalhes das tintas com cor 'cinza':")
    print(lista_tintas_by_cor("cinza"))
