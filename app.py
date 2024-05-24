import data.prepare as data_prep
from loaders.md_loader import load_data
from config import TMP_DATA_SOURCE_PATH
from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate
from prompts.pre_prompt import PREPROMPT


llm = Ollama(model="llama3")
prompt = PromptTemplate.from_template(PREPROMPT)

data_prep.run()
index = load_data(TMP_DATA_SOURCE_PATH)

query = input("What would you like to know about us? ")

response = index.query(prompt.format(query=query), llm=llm)

print(response)
