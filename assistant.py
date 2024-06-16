import asyncio
from typing import Optional, Dict, Any, AsyncGenerator
import data.prepare as data_prep
from vector_store.index import VectorStore
from config import TMP_DATA_SOURCE_PATH, MODEL_NAME
from langchain_core.prompts import PromptTemplate
from prompts.pre_prompt import PREPROMPT
from langchain_community.llms import LlamaCpp
from langchain_core.callbacks import CallbackManager
from langchain_core.callbacks.base import BaseCallbackHandler


class CustomStreamingHandler(BaseCallbackHandler):
    def on_llm_new_token(self, token, **kwargs):
        print(f">>>>>>>({token})<<<<<<<")


class Assistant:
    def __init__(self):
        self.callback_manager = CallbackManager([CustomStreamingHandler()])
        self.llm = LlamaCpp(
            model_path="/Users/razvan/llms/ggml-model-Q8_0.gguf",  # TODO: Fix ~ expansion not working
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
        self.prompt_template = PromptTemplate.from_template(PREPROMPT)

    def __formatted_query_for(self, question, context):
        return self.prompt_template.format(query=question, context=context)

    async def ask(self, question: str) -> AsyncGenerator[str, None]:
        try:
            results = self.vector_store_index.query(question, llm=self.llm)
            context = " ".join(
                [getattr(doc, "page_content", str(doc)) for doc in results]
            )
            formatted_query = self.__formatted_query_for(question, context)
            async for token in self.llm.astream(formatted_query):
                yield token
        except Exception as e:
            print(e)
            yield f"An error occurred: {e}"

    def should_exit(self, question: str) -> bool:
        return question.strip().lower() == "/bye"

    def say_goodbye(self):
        print("Goodbye!")
