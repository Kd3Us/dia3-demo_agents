import streamlit as st
from llm_agent import ask_llm


st.set_page_config(page_title="Jarvis")
st.title("Barbe-Quasar")


# Historique affiché, propre à la session du navigateur :
# il survit aux reruns mais repart à zéro si on recharge la page
if "messages" not in st.session_state:
	st.session_state.messages = []


user_input = st.chat_input(
	"Que veux tu moussaillon ?",
	accept_file=False,
	accept_audio=False
	)

if user_input :
	response = ask_llm(user_input)
	st.session_state.messages.append({"role": "user", "content": user_input})
	st.session_state.messages.append({"role": "assistant", "content": response})

for message in st.session_state.messages:
	with st.chat_message(message["role"]):
		st.markdown(message["content"])
