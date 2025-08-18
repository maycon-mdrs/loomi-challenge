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


def dalle_tool(prompt: str):
    """
    Ferramenta para integração com o agente supervisor/workflow.
    Recebe um prompt e retorna a imagem gerada.

    Parâmetros:
    - prompt (str): Descrição do ambiente, cor, acabamento ou qualquer detalhe relevante para gerar a imagem.
    """
    image_url = generate_dalle_image(prompt)
    return {"image_url": image_url, "prompt": prompt}
