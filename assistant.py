import asyncio
from typing import Optional, Dict, Any, AsyncGenerator
import data.prepare as data_prep
from vector_store.index import VectorStore
from config import TMP_DATA_SOURCE_PATH, TEMPERATURE, TOP_P, MAX_TOKENS
from langchain_core.prompts import PromptTemplate
from langchain_community.llms import LlamaCpp
from langchain_core.callbacks import CallbackManager
from custom_streaming_handler import CustomStreamingHandler


class Assistant:
    def __init__(self, model_path):
        self.callback_manager = CallbackManager([CustomStreamingHandler()])
        self.llm = LlamaCpp(
            model_path=model_path,
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS,
            top_p=TOP_P,
            callback_manager=self.callback_manager,
            verbose=False,
        )
        data_prep.run()
        self.vector_store_index = VectorStore(
            path=TMP_DATA_SOURCE_PATH
        ).build_vector_store()

    def set_streaming_handler(self, streaming_handler):
        for handler in self.callback_manager.handlers:
            if isinstance(handler, CustomStreamingHandler):
                handler.handler_function = streaming_handler

    def ask(self, question):
        try:
            return self.vector_store_index.query(question, llm=self.llm)
        except Exception as e:
            print(e)
            return f"An error occurred: {e}"

    def should_exit(self, question: str) -> bool:
        return question.strip().lower() == "/bye"

    def say_goodbye(self):
        print("Goodbye!")
