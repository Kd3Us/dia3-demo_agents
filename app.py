import streamlit as st
from llm_agent import LLMAgent


@st.cache_resource
def get_agent():
	return LLMAgent(context_path="./context.txt")


agent = get_agent()


st.set_page_config(page_title="Jarvis")
st.title("Barbe-Quasar")


# Historique affiché, propre à la session du navigateur
if "messages" not in st.session_state:
	st.session_state.messages = []


user_input = st.chat_input(
	"Que veux tu moussaillon ?",
	accept_file=False,
	accept_audio=False
	)

if user_input :
	response = agent.ask(user_input)
	st.session_state.messages.append({"role": "user", "content": user_input})
	st.session_state.messages.append({"role": "assistant", "content": response})

for message in st.session_state.messages:
	with st.chat_message(message["role"]):
		st.markdown(message["content"])
