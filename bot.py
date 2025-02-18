# import modules

from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from cleaner import clean_corpus

CORPUS_FILE = "chat.txt"

chatbot = ChatBot("Chatpot")

trainer = ListTrainer(chatbot)
cleaned_corpus = clean_corpus(CORPUS_FILE)
trainer.train(cleaned_corpus)

exit_conditions = (":q", "quit", "exit", "bye", "goodbye")

while True:
    query = input("You: ")
    if query.lower() in exit_conditions:
        break
    else:
        print(f"Chatbot: {chatbot.get_response(query)}")