"""Streamlit front end for the LLM OOP project. Run: streamlit run app.py"""
import streamlit as st

from conversation import Conversation
from exceptions import InvalidPromptError
from main import build_manager
from models import GPTModel, LanguageModel, LlamaModel

st.set_page_config(page_title="LLM Manager", page_icon="💬", layout="wide")

# ---------- session state ----------
if "manager" not in st.session_state:
    st.session_state.manager = build_manager()
    st.session_state.conversations = {}
    st.session_state.usage = {}

manager = st.session_state.manager

# ---------- sidebar ----------
with st.sidebar:
    st.title("Models")
    model_name = st.radio("Select a model", list(manager.models), label_visibility="collapsed")
    model = manager.get_model(model_name)
    st.caption(f"{model.provider} · {len(model):,} token limit")

    st.subheader("Settings")
    model.temperature = st.slider("Temperature", 0.0, 2.0, float(model.temperature), 0.1,
                                  key=f"temp_{model_name}")
    model.is_active = st.toggle("Model active", value=model.is_active, key=f"active_{model_name}")

    if st.button("Clear conversation"):
        st.session_state.conversations.pop(model_name, None)
        st.session_state.usage.pop(model_name, None)

    with st.expander("Select best model (ModelManager)"):
        providers = sorted({m.provider for m in manager.models.values()})
        provider = st.selectbox("Provider", providers)
        required = st.number_input("Required tokens", min_value=1, value=5000, step=500)
        best = manager.select_model(provider, int(required))
        if best:
            st.success(f"Selected: {best.model_name}")
        else:
            st.warning("No active model fits.")

# ---------- per-model conversation ----------
if model_name not in st.session_state.conversations:
    st.session_state.conversations[model_name] = Conversation(
        list(manager.models).index(model_name) + 1, model)
    st.session_state.usage[model_name] = {"tokens": 0, "cost": 0.0}

conversation = st.session_state.conversations[model_name]
usage = st.session_state.usage[model_name]

# ---------- handle input (before rendering so errors show immediately) ----------
error = None
prompt = st.chat_input(f"Message {model_name}", disabled=not model.is_active)
if prompt is not None:
    try:
        model.validate_prompt(prompt)
        tokens = model.tokenizer.count_tokens(prompt)
        if tokens > model.max_tokens:
            raise InvalidPromptError(f"This model accepts up to {model.max_tokens:,} tokens.")
        conversation.send_message(prompt)
        usage["tokens"] += tokens
        usage["cost"] += model.calculate_request_cost(prompt)
    except InvalidPromptError as exc:
        error = str(exc)

# ---------- main area ----------
st.title(f"{model_name}")
chat_tab, info_tab = st.tabs(["Chat", "Model info"])

with chat_tab:
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Messages sent", len(conversation.messages) // 2)
    c2.metric("Input tokens", f"{usage['tokens']:,}")
    c3.metric("Estimated cost", f"${usage['cost']:.6f}")
    c4.metric("Models created", LanguageModel.get_total_models())

    if not model.is_active:
        st.info("This model is inactive. Turn it on in the sidebar to chat.")
    if error:
        st.error(f"InvalidPromptError: {error}")
    if not conversation.messages:
        st.caption("Simulated chat. One word counts as one token.")

    for message in conversation.messages:
        with st.chat_message(message["role"]):
            st.text(message["content"])

with info_tab:
    left, right = st.columns(2)
    plan = model.pricing_plan

    with left:
        st.subheader("display_info()")
        st.code(
            f"Model Name: {model.model_name}\n"
            f"Provider: {model.provider}\n"
            f"Maximum Tokens: {model.max_tokens}\n"
            f"Temperature: {model.temperature}",
            language="text")

        st.subheader("Class details")
        details = {
            "Class": type(model).__name__,
            "Parent classes": ", ".join(c.__name__ for c in type(model).__bases__),
            "Active": str(model.is_active),
        }
        if isinstance(model, GPTModel):
            details["API key"] = "*" * len(model.api_key)
        if isinstance(model, LlamaModel):
            details["Model path"] = model.model_path
            details["Quantization"] = model.quantization
        st.table(details)

    with right:
        st.subheader("Pricing plan")
        st.write(f"`{plan.plan_name}` at {plan.price_per_1000_tokens} USD per 1000 tokens")

        st.subheader("Request cost calculator")
        text = st.text_area("Prompt", "Explain machine learning")
        if text.strip():
            n = model.tokenizer.count_tokens(text)
            st.code(f"Input tokens: {n}\nRequest cost: ${plan.calculate_cost(n):.6f}", language="text")