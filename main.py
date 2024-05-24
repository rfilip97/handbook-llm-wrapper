from assistant import Assistant

assistant = Assistant()

while True:
    question = input("\n(AI) What would you like to know about us?\n> ")

    if assistant.should_exit(question):
        assistant.say_goodbye()
        break

    answer = assistant.ask(question)
    print(f"\n{answer}")
