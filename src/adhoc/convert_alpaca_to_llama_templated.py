"""
This file essentially converts a passed in Alpaca formatted dataset, to a tokenized Llama formatted dataset. 
"""
# this is the arbritary path include import
import sys, os; sys.path.append(os.getcwd()) if os.getcwd() not in sys.path else None
from transformers import AutoTokenizer
import src.utils as utils
import argparse

configurations = utils.read_env_file()

def tokenize_data(data):
    tokenizer = AutoTokenizer.from_pretrained(configurations['MODEL'])
    for i in range(len(data)):
        data[i] = [{"role" : "user", "content" : data[i]["input"]}, {"role" : "assistant", "content" : data[i]["output"]}]
    tokenized_data = []
    for i in range(len(data)):
        tokenized_data.extend(tokenizer.apply_chat_template([data[i]], tokenize=False))
    return tokenized_data
    

def main(input_file, output_file=None):
    # Your conversion code here
    if output_file is None:
        output_file = input_file.split('.')[0] + '_processed.json'
    # Save your processed data to output_file
    input_file = utils.read_json_file(input_file)
    tokenized_data = tokenize_data(input_file)
    utils.write_json_file(output_file, tokenized_data)
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert Alpaca formatted dataset to Llama formatted dataset.')
    parser.add_argument('input_file', type=str, help='The path to the input file.')
    parser.add_argument('--output_file', type=str, help='The path to the output file. If not specified, the output file will be the input file name with "_processed" appended.')
    args = parser.parse_args()

    main(args.input_file, args.output_file)
