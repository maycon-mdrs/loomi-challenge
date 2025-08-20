from openai import OpenAI


def generate_dalle_image(prompt: str, model_name: str = "dall-e-3"):
    """
    Gera uma imagem usando o modelo DALL·E da OpenAI a partir de um prompt de texto.
    Retorna a URL ou base64 da imagem gerada.
    """
    client = OpenAI()
    response = client.images.generate(
        model=model_name,
        prompt=prompt,
        n=1,
        size="1024x1024",
        response_format="url",  # or "b64_json" to base64
    )
    if response and response.data:
        return response.data[0].url
    return None

# https://platform.openai.com/docs/guides/prompt-engineering
def dalle_tool(prompt: str):
    """
    Ferramenta para integração com o agente supervisor/workflow.
    Recebe um prompt e retorna a imagem gerada.

    Parâmetros:
    - prompt (str): Descrição do ambiente, cor, acabamento ou qualquer detalhe relevante para gerar a imagem.
    """
    
    _prompt = (
        f"Crie uma imagem de design com foco em tinta suveníl: {prompt}\n"
        "<prioridade> O foco principal deve ser a parede e a qualidade do acabamento da tinta, como elemento dominante. </prioridade>\n"
        "<tipo_superfície> Mostre superfície impecável, acabamento premium, textura suave e aplicação profissional, sem imperfeições. Realce o brilho acetinado ou semibrilho, saturação e profundidade da cor. </tipo_superfície>\n"
        "<diretizes_de_composição> Poucos ou sem móveis/decorativos que não distraiam, composição limpa e sem pessoas ou animais. </diretizes_de_composição>\n"
        "<especificações_de_imagem> Imagem em altíssima resolução, cores realistas, sem marcas ou logotipos. </especificações_de_imagem>\n"
    )
    
    image_url = generate_dalle_image(_prompt)
    return {"image_url": image_url, "prompt": _prompt}
