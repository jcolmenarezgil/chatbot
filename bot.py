# Import necessary modules
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.logic import BestMatch
import random
import re

# Constants
CORPUS_FILE = "text.txt"

def main():
    chatbot = ChatBot(
        "ChatBot",
        logic_adapters=[
            {
                "import_path": "chatterbot.logic.BestMatch",
                "default_response": "I don't understand what you're saying. Can you rephrase your question?",
                "maximum_similarity_threshold": 0.50
            }
        ]
    )

    trainer = ListTrainer(chatbot)

    try:
        cleaned_corpus = clean_corpus(CORPUS_FILE)
        print(cleaned_corpus)
        

        # Convertir a minúsculas ANTES de entrenar
        cleaned_corpus = [line.lower() for line in cleaned_corpus]

        # Asegúrate de que cleaned_corpus sea una lista de cadenas
        if isinstance(cleaned_corpus, tuple): # Si es una tupla, conviértela a lista
            cleaned_corpus = list(cleaned_corpus)

        # Entrena PRIMERO con el corpus en inglés
        trainer.train([
            'chatterbot.corpus.english.greeting',
            'chatterbot.corpus.custom.myown',
            'chatterbot.corpus.swedish.food'
        ])

        # LUEGO entrena con tus datos limpios
        trainer.train(cleaned_corpus)

        print("Corpus cargados exitosamente.")
    except Exception as e:
        print(f"Error al cargar los corpus: {e}")


    exit_conditions = (":q", "quit", "exit", "bye", "goodbye")

    while True:
        query = input("You: ")
        response = chatbot.get_response(query)
        if isinstance(response, list): 
            respuesta_seleccionada = seleccionar_respuesta_aleatoria(response)
            if respuesta_seleccionada:
                print(f"Chatbot: {respuesta_seleccionada}")
            else:
                print(f"Chatbot: {chatbot.logic_adapters[0].default_response}")
        else:
            print(f"Chatbot: {response}")

def remove_chat_metadata(text_content):

    remove_dates = r"\b\d{1,2}/\d{1,2}\b"
    remove_hours = r"\b\d{1,2}:\d{2}\s*(AM|PM)?\b"
    # Expresión regular para eliminar metadatos (incluye nombres de usuario)
    pattern = r"(\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s*[AP]M\s*-\s*)?([\w\s@.,]+:\s)?"
    cleaned_text = re.sub(pattern, "", text_content)

    # Elimina fechas y horas
    cleaned_text = re.sub(remove_dates, "", cleaned_text)
    cleaned_text = re.sub(remove_hours, "", cleaned_text)

    # Elimina espacios en blanco adicionales y líneas vacías
    cleaned_lines = [line.strip() for line in cleaned_text.splitlines() if line.strip()]
    return cleaned_lines

def remove_non_message_text(text_lines):
    if not text_lines:  # Maneja el caso de que no haya líneas
        return []

    messages = text_lines[1:-1] if len(text_lines) > 2 else text_lines # Maneja archivos con menos de 3 líneas

    filter_out_msgs = ("<Media omitted>",)
    return [msg.strip() for msg in messages if msg not in filter_out_msgs and msg.strip()]

def clean_corpus(chat_export_file):
    try:
        with open(chat_export_file, "r", encoding="utf-8") as corpus_file:
            content = corpus_file.read()
    except UnicodeDecodeError:
        print(f"Error: Could not decode {chat_export_file} with UTF-8. Trying other encodings.")
        try:
            with open(chat_export_file, "r", encoding="latin-1") as corpus_file:
                content = corpus_file.read()
        except UnicodeDecodeError:
            print(f"Error: Could not decode {chat_export_file} with latin-1. Trying other encodings.")
            try:
                with open(chat_export_file, "r", encoding="cp1252") as corpus_file:
                    content = corpus_file.read()
            except UnicodeDecodeError:
                print(f"Error: Could not decode {chat_export_file} with cp1252. Trying other encodings.")
                try:
                    with open(chat_export_file, "r", encoding="utf-16") as corpus_file:
                        content = corpus_file.read()
                except UnicodeDecodeError:
                    print(f"Error: Could not decode {chat_export_file} with utf-16. Giving up.")
                    return []  # Devuelve una lista vacía si falla la decodificación

    message_corpus = remove_chat_metadata(content)
    cleaned_corpus = remove_non_message_text(message_corpus)
    return cleaned_corpus
   
def seleccionar_respuesta_aleatoria(responses):
    if responses:
        return random.choice(responses)
    return None

# Entry point of the program
# This is the main function that runs the chatbot
if __name__ == "__main__":
    main()