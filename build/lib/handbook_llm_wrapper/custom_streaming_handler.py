from langchain_core.callbacks.base import BaseCallbackHandler


class CustomStreamingHandler(BaseCallbackHandler):
    def __default_handler_function(token):
        print(f"Token: [{token}]")

    def __init__(self, handler_function=__default_handler_function):
        self.handler_function = handler_function

    def on_llm_new_token(self, token, **kwargs):
        self.handler_function(token)

    def set_handler_function(self, handler_function):
        self.handler_function = handler_function
