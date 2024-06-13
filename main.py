import asyncio
from assistant import Assistant


async def main():
    assistant = Assistant()
    question = input("Enter your question (or type '/bye' to exit): ")

    while not assistant.should_exit(question):
        async for token in assistant.ask(question):
            pass  # Tokens are printed by the custom handler
        question = input("Enter your question (or type '/bye' to exit): ")
    assistant.say_goodbye()


if __name__ == "__main__":
    asyncio.run(main())
