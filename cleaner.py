# cleaner.py

import re

def clean_corpus(chat_export_file):
    message_corpus = remove_chat_metadata(chat_export_file)
    cleaned_corpus = remove_non_message_text(message_corpus)
    return cleaned_corpus

def remove_chat_metadata(chat_export_file):
    date_time = r"(\d+\/\d+\/\d+,\s\d+:\d+)"  # e.g. "9/16/22, 06:34"
    dash_whitespace = r"\s-\s"  # " - "
    username = r"([\w\s]+)"  # e.g. "Martin"
    metadata_end = r":\s"  # ": "
    pattern = date_time + dash_whitespace + username + metadata_end

    try:
        with open(chat_export_file, "r", encoding="utf-8") as corpus_file:  # Specify UTF-8 encoding
            content = corpus_file.read()
    except UnicodeDecodeError:
        print(f"Error: Could not decode {chat_export_file} with UTF-8. Trying other encodings.")
        try:
           with open(chat_export_file, "r", encoding="latin-1") as corpus_file: # Try latin-1
               content = corpus_file.read()
        except UnicodeDecodeError:
            print(f"Error: Could not decode {chat_export_file} with latin-1. Trying other encodings.")
            try:
                with open(chat_export_file, "r", encoding="cp1252") as corpus_file: # Try cp1252
                    content = corpus_file.read()
            except UnicodeDecodeError:
                print(f"Error: Could not decode {chat_export_file} with cp1252. Trying other encodings.")
                with open(chat_export_file, "r", encoding="utf-16") as corpus_file: # Try utf-16
                    content = corpus_file.read()
                    
    cleaned_corpus = re.sub(pattern, "", content)
    return tuple(cleaned_corpus.split("\n"))

def remove_non_message_text(export_text_lines):
    messages = export_text_lines[1:-1]

    filter_out_msgs = ("<Media omitted>",)
    return tuple((msg for msg in messages if msg not in filter_out_msgs))
