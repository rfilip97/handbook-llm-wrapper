import asyncio
import argparse
import os
from assistant import Assistant


async def main(model_path):
    assistant = Assistant(model_path=model_path)
    question = input("Enter your question (or type '/bye' to exit): ")

    while not assistant.should_exit(question):
        async for token in assistant.ask(question):
            pass  # Tokens are printed by the custom handler
        question = input("Enter your question (or type '/bye' to exit): ")
    assistant.say_goodbye()


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

    asyncio.run(main(model_path))
