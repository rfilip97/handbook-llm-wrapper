from langchain_community.llms import Ollama
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain

llm = Ollama(model="llama3")

template = """
Provide the number of legs the following animal has, or
type 'NONE' if it doesn't apply. Please always respond only
with either a number which is the response, or with NONE

text: {input}
"""

prompt_template = ChatPromptTemplate.from_template(template=template)
chain = LLMChain(llm=llm, prompt=prompt_template)

user_input = input("Please enter the text you want to process: ")
response = chain.predict(input=user_input)

print(response)

