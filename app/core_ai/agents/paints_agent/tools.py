from app.database.connection import Session
from app.services.paint_retriever_rag_service import PaintRetrieverRagService
from app.services.paint_service import PaintService
from app.DTOs.paint_dtos import PaintResponse

retriever_service = PaintRetrieverRagService()


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
