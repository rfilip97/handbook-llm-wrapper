import argparse
import os
from assistant import Assistant


def streaming_handler(token):
    print(f"----({token})----")


def main(model_path):
    assistant = Assistant(model_path=model_path)
    assistant.set_streaming_handler(streaming_handler)

    while True:
        question = input("\n(AI) What would you like to know about us?\n> ")

        if assistant.should_exit(question):
            assistant.say_goodbye()
            break

        answer = assistant.ask(question)
        print(f"\n{answer}")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Run the assistant with a specific model path."
    )
    parser.add_argument(
        "--model_path", type=str, help="Path to the model file", required=True
    )

    args = parser.parse_args()

    return args


if __name__ == "__main__":
    args = parse_args()
    model_path = os.path.expanduser(args.model_path)

    main(model_path)
