from langchain_community.llms import Ollama

llm = Ollama(model="llama3")

response = llm.invoke("What is the meaning of life?")

print(response)

