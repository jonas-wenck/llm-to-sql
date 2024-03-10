from transformers import AutoModelForCausalLM, AutoTokenizer
import test_data
import os
import torch
from dotenv import load_dotenv

load_dotenv()

hf_cache_directory = os.getenv("HF_CACHE_DIRECTORY")

tokenizer = AutoTokenizer.from_pretrained("microsoft/phi-2", cache_dir=hf_cache_directory)
model = AutoModelForCausalLM.from_pretrained("microsoft/phi-2", torch_dtype=torch.float32, cache_dir=hf_cache_directory)

prompt = ("You will be given the DDL of a table structure. You task is to generate a SQL statement that solves a given task.\
    This is the table structure:" + test_data.SCHEMA + "\
    This is your task: " + test_data.QUESTION)

inputs = tokenizer("Instruct: " + prompt + "\nOutput:", return_tensors="pt", return_attention_mask=False)

outputs = model.generate(**inputs, max_length=200)
response = tokenizer.batch_decode(outputs)[0]
print(response)
