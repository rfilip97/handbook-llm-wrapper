import asyncio
from langchain_community.llms import Ollama
from langchain.prompts import ChatPromptTemplate


async def main():
    llm = Ollama(model="llama3")

    template = """
    Please respond to the question in a funny way

    question: {input}
    """

    prompt = ChatPromptTemplate.from_template(template=template)

    user_input = input("Please enter the text you want to process: ")

    chain = prompt | llm

    response = ""
    async for chunk in chain.astream({"input": user_input}):
        response += chunk

        # Clear the screen #HACKERMAN
        print("\033[2J\033[H", end="")
        print(response, end="", flush=True)


if __name__ == "__main__":
    asyncio.run(main())
