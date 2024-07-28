import sys, os; sys.path.append(os.getcwd()) if os.getcwd() not in sys.path else None
from openai import OpenAI
import tiktoken
import concurrent.futures
import re
from src import utils
import asyncio
import aiohttp
import tempfile
import logging
from tqdm.asyncio import tqdm

configurations = utils.read_env_file()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def num_tokens_from_string(string: str, encoding_name: str) -> int:
    encoding = tiktoken.get_encoding(encoding_name)
    return len(encoding.encode(string))

def sentence_tokenize(text):
    return re.findall(r'[^.!?]+[.!?]', text)

def word_count(text):
    return len(text.split())

def chunk_text(file_path, chunk_size=1024):
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

async def process_chunk(chunk, system_prompt, user_prompt, session, model):
    try:
        message = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt.format(chunk)}
        ]
        async with session.post(f"{configurations['OPENAI_BASE_URL']}/chat/completions", json={
            "model": model,
            "messages": message,
            "temperature": 1.25,
            "max_tokens": 4096,
        }) as response:
            result = await response.json()
            return result['choices'][0]['message']['content']
    except Exception as e:
        logging.error(f"Error processing chunk: {e}")
        return ""

async def main():
    data_dir = os.path.join(configurations["DATA_ROOT"], "source_data")
    files = utils.get_all_txt_files_in_dirs_and_subdirs(data_dir)
    chunks = []
    for file in files:
        chunks.extend(chunk_text(file))
    
    system_prompt = utils.read_text_file(os.path.join(configurations["DATA_ROOT"], "prompts", "qa_generation_system_prompt.txt"))
    user_prompt = utils.read_text_file(os.path.join(configurations["DATA_ROOT"], "prompts", "qa_generation_user_prompt.txt"))
    model = configurations["DATAGEN_MODEL"]
    chunks = chunks[:100]  # For testing, remove this line for full processing
    
    async with aiohttp.ClientSession(headers={"Authorization": f"Bearer {configurations['OPENAI_API_KEY']}"}) as session:
        tasks = [process_chunk(chunk, system_prompt, user_prompt, session, model) for chunk in chunks]
        answers = []
        for f in tqdm.as_completed(tasks, total=len(tasks), desc="Processing chunks"):
            answer = await f
            answers.append(answer)
    
    output_file = os.path.join(configurations["DATA_ROOT"], "generated_data", "qa_pairs.txt")
    with open(output_file, 'w', encoding='utf-8') as f:
        for answer in answers:
            if answer:  # Only write non-empty answers
                f.write(answer + "\n\n")
    
    logging.info(f"Processed {len(chunks)} chunks. Results written to {output_file}")

if __name__ == "__main__":
    asyncio.run(main())
    