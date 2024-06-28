import argparse
import os
from handbook_llm_wrapper.assistant import Assistant


def streaming_handler_function(token):
    print(f"----({token})----")


def create_assistant(model_path):
    assistant = Assistant(model_path=model_path)
    assistant.set_streaming_handler_function(streaming_handler_function)
    return assistant


def ask_question(assistant, question):
    if assistant.should_exit(question):
        assistant.say_goodbye()
        return "Goodbye!"

    return assistant.ask(question)


def interactive_mode(model_path):
    assistant = create_assistant(model_path)

    while True:
        question = input("\n(AI) What would you like to know about us?\n> ")

        answer = ask_question(assistant, question)
        print(f"\n{answer}")

        if answer == "Goodbye!":
            break


def parse_args():
    parser = argparse.ArgumentParser(
        description="Run the assistant with a specific model path."
    )

    parser.add_argument(
        "--model_path", type=str, help="Path to the model file", required=True
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    model_path = os.path.expanduser(args.model_path)
    interactive_mode(model_path)
