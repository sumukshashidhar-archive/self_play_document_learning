import sys, os; sys.path.append(os.getcwd()) if os.getcwd() not in sys.path else None
from src import utils
from transformers import AutoTokenizer

configurations = utils.read_env_file() 

def main(source_data, output_data, json_convo_data, model):
   text_files = utils.get_all_txt_files_in_dirs_and_subdirs(source_data)
   json_files = utils.get_all_json_files_in_dirs_and_subdirs(json_convo_data)
   chunks = [utils.chunk_text(file) for file in text_files] + [utils.chunk_text(file, 1024) for file in text_files] + [utils.chunk_text(file, 512) for file in text_files]
   chunked = []
   for each_chunk in chunks:
      chunked.extend(each_chunk)
   # tokenize
   tokenizer = AutoTokenizer.from_pretrained(model)
   tokenized = [tokenizer.bos_token + chunk + tokenizer.eos_token for chunk in chunked]
   for json_file in json_files:
      data = utils.read_text_file(json_file)
      data = eval(data)
      chunked.extend(data)
   print(len(chunked))
   # write to json file
   utils.write_json_file(output_data, chunked)
   

if __name__ == "__main__":
    source_data = os.path.join(configurations["DATA_ROOT"], "source_data")
    output_data = os.path.join(configurations["DATA_ROOT"], "generated_data", "pretrain_data.json")
    json_convo_data = os.path.join(configurations["DATA_ROOT"], "weak_conversational_data")
    main(source_data, output_data, json_convo_data, configurations["MODEL"])