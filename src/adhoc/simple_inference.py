"""
A simple inference script
"""
import sys, os; sys.path.append(os.getcwd()) if os.getcwd() not in sys.path else None
import transformers
import torch
from src import utils

configurations = utils.read_env_file()

model_id = configurations["MODEL"]

pipeline = transformers.pipeline(
    "text-generation",
    model=model_id,
    model_kwargs={"torch_dtype": torch.bfloat16},
    device_map="auto",
)

messages = [
    {"role": "user", "content": "You are a pirate chatbot who always responds in pirate speak! Who are you?"},
]

outputs = pipeline(
    messages,
    max_new_tokens=256,
)

print(outputs[0]["generated_text"][-1])