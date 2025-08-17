# Função para ler o conteúdo de um arquivo txt
def read_system_prompt_from_file(file_path: str) -> str:
    with open(file_path, "r") as file:
        return file.read().strip()
