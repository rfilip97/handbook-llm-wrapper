import asyncio
from langchain_community.llms import Ollama
from langchain.prompts import ChatPromptTemplate


async def main():
    llm = Ollama(model="llama3")

    initial_template = """
    You are a funny assistant. Continue the conversation based on the history.

    {conversation_history}
    User: {input}
    Assistant:
    """

    prompt = ChatPromptTemplate.from_template(template=initial_template)
    conversation_history = ""

    while True:
        user_input = input(
            "\nPlease enter the text you want to process (or type 'exit' to quit): "
        )

        if user_input.lower() == "exit":
            break

        chain = prompt | llm

        response = ""
        async for chunk in chain.astream(
            {"conversation_history": conversation_history, "input": user_input}
        ):
            response += chunk

            # Clear the screen
            print("\033[2J\033[H", end="")
            print(response, end="", flush=True)

        conversation_history += f"User: {user_input}\nAssistant: {response}\n"


if __name__ == "__main__":
    asyncio.run(main())
