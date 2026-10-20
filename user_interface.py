import streamlit as st 
from llm_agent import ConversationAgent


AVATARS = {
	"user": "🧑‍🚀",
	"assistant": "🏴‍☠️",
}

WELCOME_MESSAGE = (
	"Ahoy, moussaillon ! Bienvenue à bord de *La Vieille Rancune*. "
	"Je suis le Capitaine Vexo Barbe-Quasar. Pose ta question, montre-moi une image "
	"ou parle-moi directement... mais fais vite, les patrouilles ne sont jamais loin."
)


class UserInterface:
	def __init__(self):
		st.set_page_config(page_title="Jarvis")
		st.title("Barbe-Quasar")
		self.conversation_agent_object = self.get_persistant_conversation_agent()
		self.displayed_history = self.get_persistant_displayed_history()


	def get_persistant_conversation_agent(self):

		if "conversation_agent_object" not in st.session_state:
			st.session_state.conversation_agent_object = ConversationAgent()

		return st.session_state.conversation_agent_object


	def get_persistant_displayed_history(self):

		if "displayed_history" not in st.session_state:
			st.session_state.displayed_history = [
				{"role": "assistant", "text": WELCOME_MESSAGE, "image": None}
			]

		return st.session_state.displayed_history


	def update_displayed_history(self, role, text, image=None):
		self.displayed_history.append(
			{
			"role": role,
			"text": text,
			"image": image,
			}
		)


	@staticmethod
	def show_message(role, text, image=None):
		with st.chat_message(role, avatar=AVATARS[role]):
			if image is not None:
				st.image(image)
			st.markdown(text)


	def show_discussion_history(self):
		for message in self.displayed_history:
			self.show_message(message["role"], message["text"], message["image"])


	def get_text_interaction(self, user_input):
		if user_input.audio:
			with st.spinner("Le Capitaine tend l'oreille..."):
				return self.conversation_agent_object.transcribe_audio(user_input.audio)

		return user_input.text


	@staticmethod
	def get_image_file(user_input):
		if user_input.files:
			return user_input.files[0]

		return None


	def show_streamed_response(self, text_interaction, image_file):
		with st.chat_message("assistant", avatar=AVATARS["assistant"]):
			with st.spinner("Le Capitaine consulte ses cartes stellaires..."):
				stream = self.conversation_agent_object.ask_llm_stream(text_interaction, image_file)
			return st.write_stream(stream)


	def run(self):
		self.show_discussion_history()

		user_input = st.chat_input(
			"Que veux tu moussaillon ?",
			accept_file=True,
			file_type=["jpg", "jpeg", "png"],
			accept_audio=True,
			submit_mode="disable",
			)

		if user_input :
			text_interaction = self.get_text_interaction(user_input)
			image_file = self.get_image_file(user_input)

			if image_file is not None and not text_interaction:
				text_interaction = "Décris cette image."

			image = image_file.getvalue() if image_file is not None else None
			self.update_displayed_history(role="user", text=text_interaction, image=image)
			self.show_message("user", text_interaction, image)

			response = self.show_streamed_response(text_interaction, image_file)
			self.update_displayed_history(role="assistant", text=response)



if __name__ == "__main__":
	user_interface_object = UserInterface()
	user_interface_object.run()








































	# response = ask_llm(user_input)
	# with st.chat_message("user"):
	# 	st.markdown(user_input)

	# with st.chat_message("system"):
	# 	st.markdown(response)


