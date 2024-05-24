from assistant import Assistant

assistant = Assistant()

while True:
    question = input("What would you like to know about us? ")
    answer = assistant.ask(question)

    print(answer)
