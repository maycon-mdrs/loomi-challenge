from app.database.connection import Session
from app.services.paint_service import PaintService
from app.DTOs.paint_dtos import PaintResponse


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
            {"id": paint.id, "paint_name": paint.paint_name}
            for paint in paints
        ]
    finally:
        db_session.close()
        

def lista_tinta_by_name(nome_tinta: str):
    """
    Recupera detalhes de uma tinta específica com base no nome fornecido.
    
    Parâmetros:
    - nome_tinta (str): Nome da tinta que se deseja consultar. Pode ser obtido a partir da função `lista_tintas`.
    """
    db_session = Session()
    try:
        paint_service = PaintService(db_session)
        paint = paint_service.get_paint_by_name(name=nome_tinta)
        if not paint:
            return None
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
    print("Lista de tintas disponíveis:")
    print(lista_tintas())
    
    print("\n\nDetalhes da tinta com ID 1:")
    print(lista_tinta_by_id(1))
    
    print("\n\nDetalhes da tinta com nome 'Suvinil Toque de Seda':")
    print(lista_tinta_by_name("Suvinil toque de seda"))
