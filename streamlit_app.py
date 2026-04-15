import requests
import streamlit as st


st.set_page_config(page_title="PintAI Tester", page_icon="🎨", layout="wide")

DEFAULT_API_URL = "http://localhost:8000"
LOGIN_PATH = "/api/v1/auth/login"
CHAT_PATH = "/api/v1/chat/"


def reset_chat() -> None:
    st.session_state.chat_id = None
    st.session_state.messages = []


if "token" not in st.session_state:
    st.session_state.token = None
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "chat_id" not in st.session_state:
    st.session_state.chat_id = None
if "messages" not in st.session_state:
    st.session_state.messages = []


st.title("🎨 PintAI - Teste Rápido com Streamlit")
st.caption("Cliente simples para autenticar e conversar com a API.")

with st.sidebar:
    st.header("Configuração")
    api_base_url = st.text_input("Base URL da API", value=DEFAULT_API_URL).rstrip("/")
    st.markdown("---")

    if st.session_state.token:
        st.success("Autenticado")
        st.write(f"**user_id:** {st.session_state.user_id}")
        if st.button("Sair"):
            st.session_state.token = None
            st.session_state.user_id = None
            reset_chat()
            st.rerun()
    else:
        st.info("Faça login para iniciar.")


if not st.session_state.token:
    st.subheader("Login")
    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Senha", type="password")
        submit_login = st.form_submit_button("Entrar")

    if submit_login:
        if not email or not password:
            st.error("Preencha email e senha.")
        else:
            try:
                response = requests.post(
                    f"{api_base_url}{LOGIN_PATH}",
                    json={"email": email, "password": password},
                    timeout=30,
                )
                if response.ok:
                    data = response.json()
                    st.session_state.token = data.get("token")
                    st.session_state.user_id = data.get("id")
                    reset_chat()
                    st.success("Login realizado com sucesso.")
                    st.rerun()
                else:
                    st.error(
                        f"Falha no login ({response.status_code}): {response.text}"
                    )
            except requests.RequestException as exc:
                st.error(f"Erro de conexão com a API: {exc}")
else:
    st.subheader("Chat")
    col1, col2 = st.columns([3, 1])
    with col1:
        st.write(f"**chat_id atual:** `{st.session_state.chat_id or 'novo chat'}`")
    with col2:
        if st.button("Novo chat", use_container_width=True):
            reset_chat()
            st.rerun()

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    prompt = st.chat_input("Digite sua pergunta sobre tintas...")
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        try:
            parsed_user_id = int(st.session_state.user_id)
        except (TypeError, ValueError):
            st.error(
                "O `id` retornado no login não é numérico. "
                "Ajuste o backend/DTO para enviar um id inteiro."
            )
            st.stop()

        payload = {
            "user_id": parsed_user_id,
            "chat_id": st.session_state.chat_id,
            "prompt": prompt,
        }
        headers = {"Authorization": f"Bearer {st.session_state.token}"}

        with st.chat_message("assistant"):
            with st.spinner("Consultando PintAI..."):
                try:
                    response = requests.post(
                        f"{api_base_url}{CHAT_PATH}",
                        json=payload,
                        headers=headers,
                        timeout=60,
                    )
                    if response.ok:
                        data = response.json()
                        assistant_text = data.get("response", "Sem resposta.")
                        st.session_state.chat_id = data.get("chat_id")
                        st.session_state.messages.append(
                            {"role": "assistant", "content": assistant_text}
                        )
                        st.markdown(assistant_text)
                    else:
                        error_text = (
                            f"Erro no chat ({response.status_code}): {response.text}"
                        )
                        st.session_state.messages.append(
                            {"role": "assistant", "content": error_text}
                        )
                        st.error(error_text)
                except requests.RequestException as exc:
                    error_text = f"Erro de conexão com a API: {exc}"
                    st.session_state.messages.append(
                        {"role": "assistant", "content": error_text}
                    )
                    st.error(error_text)
