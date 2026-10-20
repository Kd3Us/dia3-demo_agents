from groq import Groq

from dotenv import load_dotenv
import os

load_dotenv()


class LLMAgent:

    def __init__(self, context_path, model="openai/gpt-oss-120b"):
        self.client = Groq(api_key=os.environ["GROQ_KEY"])
        self.model = model
        self.history = [
            {
                "role": "system",
                "content": self._read_file(context_path)
            }
        ]

    @staticmethod
    def _read_file(file_path):
        with open(file_path, "r") as file:
            return file.read()

    def ask(self, question):
        self.history.append({"role": "user", "content": question})

        chat_completion = self.client.chat.completions.create(
            messages=self.history,
            model=self.model,
            include_reasoning=False,
        )

        response = chat_completion.choices[0].message.content
        self.history.append({"role": "assistant", "content": response})
        return response


if __name__ == "__main__":
    agent = LLMAgent(context_path="./context.txt")
    question = input("Pose ta question :\n")
    response = agent.ask(question)
    print("\n")
    print(response)
