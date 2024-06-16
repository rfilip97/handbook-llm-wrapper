import asyncio
from typing import Optional, Dict, Any, AsyncGenerator
import data.prepare as data_prep
from vector_store.index import VectorStore
from config import TMP_DATA_SOURCE_PATH
from langchain_core.prompts import PromptTemplate
from langchain_community.llms import LlamaCpp
from langchain_core.callbacks import CallbackManager
from langchain_core.callbacks.base import BaseCallbackHandler


class CustomStreamingHandler(BaseCallbackHandler):
    def __default_handler(token):
        print(f"Token: [{token}]")

    def __init__(self, handler_function=__default_handler):
        self.handler_function = handler_function

    def on_llm_new_token(self, token, **kwargs):
        self.handler_function(token)


class Assistant:
    def __init__(self, model_path):
        self.callback_manager = CallbackManager([CustomStreamingHandler()])
        self.llm = LlamaCpp(
            model_path=model_path,
            temperature=0,
            max_tokens=1000,
            top_p=1,
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
