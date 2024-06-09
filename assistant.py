import data.prepare as data_prep
from vector_store.index import VectorStore
from config import TMP_DATA_SOURCE_PATH, MODEL_NAME
from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate
from prompts.pre_prompt import PREPROMPT


class Assistant:
    def __init__(self):
        self.llm = Ollama(model=MODEL_NAME)
        data_prep.run()
        self.vector_store_index = VectorStore(
            path=TMP_DATA_SOURCE_PATH
        ).build_vector_store()
        self.prompt_template = PromptTemplate.from_template(PREPROMPT)

    def __formatted_query_for(self, query):
        return self.prompt_template.format(query=query)

    def ask(self, question):
        formatted_query = self.__formatted_query_for(question)

        return self.vector_store_index.query(formatted_query, llm=self.llm)

    def should_exit(self, question):
        return True if question.strip().lower() == "/bye" else False

    def say_goodbye(self):
        print("Goodbye!")
