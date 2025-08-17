from fastapi import status, HTTPException


class PaintAlreadyExistsException(HTTPException):
	def __init__(self):
		super().__init__(
			status_code=status.HTTP_409_CONFLICT,
			detail="Já existe uma tinta com esse nome!",
		)


class PaintCreationException(HTTPException):
	def __init__(self):
		super().__init__(
			status_code=status.HTTP_400_BAD_REQUEST,
			detail="Não foi possível criar a tinta",
		)


class PaintNotFoundException(HTTPException):
	def __init__(self):
		super().__init__(
			status_code=status.HTTP_404_NOT_FOUND,
			detail="Tinta não encontrada",
		)


class InvalidPaintDataException(HTTPException):
	def __init__(self):
		super().__init__(
			status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
			detail="Dados de tinta inválidos",
		)
