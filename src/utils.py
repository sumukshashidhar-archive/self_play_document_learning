import json
import logging
import tiktoken
import re


def num_tokens_from_string(string: str, encoding_name: str) -> int:
    encoding = tiktoken.get_encoding(encoding_name)
    return len(encoding.encode(string))

def sentence_tokenize(text):
    return re.findall(r'[^.!?]+[.!?]', text)

def word_count(text):
    return len(text.split())
def read_env_file(file_path='.env'):
    # set the default to be the .env file
    config = {}
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                key_value = line.split('=', 1)
                if len(key_value) == 2:
                    key, value = key_value
                    config[key] = value
    return config

def read_json_file(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data

def read_text_file(file_path):
    with open(file_path, 'r') as f:
        data = f.read()
    return data

def get_all_json_files_in_dirs_and_subdirs(dir_path):
    import os
    txt_files = []
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if file.endswith('.json'):
                txt_files.append(os.path.join(root, file))
    return txt_files


def get_all_txt_files_in_dirs_and_subdirs(dir_path):
    import os
    txt_files = []
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if file.endswith('.txt') or file.endswith('.md'):
                txt_files.append(os.path.join(root, file))
    return txt_files


def chunk_text(file_path, chunk_size=2048):
    logging.info(f"Chunking text from {file_path}")
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    sentences = sentence_tokenize(text)
    chunks = []
    current_chunk = []
    current_word_count = 0
    for sentence in sentences:
        sentence_word_count = word_count(sentence)
        if current_word_count + sentence_word_count > chunk_size and current_chunk:
            chunks.append(' '.join(current_chunk))
            current_chunk = []
            current_word_count = 0
        current_chunk.append(sentence.strip())
        current_word_count += sentence_word_count
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    logging.info(f"Created {len(chunks)} chunks from {file_path}")
    return chunks


def write_json_file(file_path, data):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

# read jsonl file function
def read_jsonl_file(file_path):
    # set the default to be the .env file
    data = []
    with open(file_path, 'r') as f:
        for line in f:
            data.append(json.loads(line))
    return data




if __name__ == "__main__":
    # print the content of the file
    print(read_env_file('.env'))