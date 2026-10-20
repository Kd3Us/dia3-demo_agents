from groq import Groq

from dotenv import load_dotenv
import os
import base64
import mimetypes


class ConversationAgent:
    def __init__(self):
        load_dotenv()
        self.groq_client = Groq(api_key=os.environ["GROQ_KEY"])
        self.conversation_history = [
                {
                    "role": "system",
                    "content": self.read_file(file_path="./context.txt")
                }
            ]


    @staticmethod
    def read_file(file_path):
        with open(file_path, "r") as file:
            return file.read()


    def get_conversation_history(self):
        return self.conversation_history[1: ]


    def update_conversation_history(self, role, content):
        self.conversation_history.append(
            {
            "role": role,
            "content": content,
            }
        )


    @staticmethod
    def build_user_content(text_interaction, image_file):
        if image_file is None:
            return text_interaction

        image_type = mimetypes.guess_type(image_file.name)[0]
        base64_image = base64.b64encode(image_file.read()).decode("utf-8")

        return [
            {"type": "text", "text": text_interaction},
            {
                "type": "image_url",
                "image_url": {"url": f"data:{image_type};base64,{base64_image}"},
            },
        ]


    def remove_old_images(self):
        for message in self.conversation_history:
            if isinstance(message["content"], list):
                texts = [part["text"] for part in message["content"] if part["type"] == "text"]
                message["content"] = "\n".join(texts) + "\n[image envoyée précédemment]"


    def ask_llm(self, text_interaction, image_file=None):

        if image_file is not None:
            self.remove_old_images()

        user_content = self.build_user_content(text_interaction, image_file)
        self.update_conversation_history(role="user", content=user_content)

        response = self.groq_client.chat.completions.create(
            messages=self.conversation_history,
            model="qwen/qwen3.8-27b",
            reasoning_effort="none",
            max_tokens=600,
        ).choices[0].message.content


        self.update_conversation_history(role="assistant", content=response)


    def transcribe_audio(self, audio_file):
        transcription = self.groq_client.audio.transcriptions.create(
            file=(audio_file.name, audio_file.read()),
            model="whisper-large-v3",
            temperature=0,
            response_format="verbose_json",
        )

        return transcription.text