from groq import Groq

from dotenv import load_dotenv
import os

load_dotenv()



def read_file(file_path):
    with open(file_path, "r") as file:
        return file.read()


# Mémoire de l'agent 
history = [
    {
        "role": "system",
        "content": read_file(file_path="./context.txt")
    }
]


def ask_llm(question):

    client = Groq(api_key=os.environ["GROQ_KEY"])

    history.append({"role": "user", "content": question})

    chat_completion = client.chat.completions.create(
        messages=history,
        model="openai/gpt-oss-120b",
        include_reasoning=False,
    )


    response = chat_completion.choices[0].message.content
    history.append({"role": "assistant", "content": response})
    return response


if __name__ == "__main__":
    question = input("Pose ta question :\n")
    response = ask_llm(question)
    print("\n")
    print(response)