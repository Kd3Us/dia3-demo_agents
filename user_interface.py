import streamlit as st 
from llm_agent import ConversationAgent


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
			st.session_state.displayed_history = []

		return st.session_state.displayed_history


	def update_displayed_history(self, role, text, image=None):
		self.displayed_history.append(
			{
			"role": role,
			"text": text,
			"image": image,
			}
		)


	def show_discussion_history(self):
		for message in self.displayed_history:
			with st.chat_message(message["role"]):
				if message["image"] is not None:
					st.image(message["image"])
				st.markdown(message["text"])


	def get_text_interaction(self, user_input):
		if user_input.audio:
			return self.conversation_agent_object.transcribe_audio(user_input.audio)

		return user_input.text


	@staticmethod
	def get_image_file(user_input):
		if user_input.files:
			return user_input.files[0]

		return None


	def run(self):
		user_input = st.chat_input(
			"Que veux tu moussaillon ?",
			accept_file=True,
			file_type=["jpg", "jpeg", "png"],
			accept_audio=True
			)

		if user_input :
			text_interaction = self.get_text_interaction(user_input)
			image_file = self.get_image_file(user_input)

			if image_file is not None and not text_interaction:
				text_interaction = "Décris cette image."

			image = image_file.getvalue() if image_file is not None else None
			self.update_displayed_history(role="user", text=text_interaction, image=image)

			self.conversation_agent_object.ask_llm(text_interaction, image_file)
			response = self.conversation_agent_object.get_conversation_history()[-1]["content"]
			self.update_displayed_history(role="assistant", text=response)

			self.show_discussion_history()



if __name__ == "__main__":
	user_interface_object = UserInterface()
	user_interface_object.run()








































	# response = ask_llm(user_input)
	# with st.chat_message("user"):
	# 	st.markdown(user_input)

	# with st.chat_message("system"):
	# 	st.markdown(response)


