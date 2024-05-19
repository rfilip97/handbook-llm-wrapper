import data.prepare as data_prep
from loaders.md_loader import load_data
from config import TMP_DATA_SOURCE_PATH
from langchain_community.llms import Ollama

llm = Ollama(model="llama3")

data_prep.run()
index = load_data(TMP_DATA_SOURCE_PATH)

query = input("What would you like to know about us? ")
response = index.query(query, llm=llm)

print(response)
