import data.prepare as data_prep
from loaders.md_loader import load_data
from config import TMP_DATA_SOURCE_PATH, MODEL_NAME
from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate
from prompts.pre_prompt import PREPROMPT


class Assistant:
    def __init__(self):
        self.llm = Ollama(model=MODEL_NAME)
        data_prep.run()
        self.index = load_data(TMP_DATA_SOURCE_PATH)
        self.prompt_template = PromptTemplate.from_template(PREPROMPT)

    def formatted_query_for(self, query):
        return self.prompt_template.format(query=query)

    def ask(self, question):
        formatted_query = self.formatted_query_for(question)

        return self.index.query(formatted_query, llm=self.llm)
