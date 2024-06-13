import asyncio
from assistant import Assistant

if __name__ == "__main__":
    assistant = Assistant()

    question = input("Enter your question (or type '/bye' to exit): ")

    while not assistant.should_exit(question):
        asyncio.run(assistant.ask(question))
        question = input("\nEnter your question (or type '/bye' to exit): ")

    assistant.say_goodbye()
