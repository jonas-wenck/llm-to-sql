from datetime import datetime
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import os
from dotenv import load_dotenv
import test_data

load_dotenv()

hf_cache_directory = os.getenv("HF_CACHE_DIRECTORY")
access_token = os.getenv("ACCESS_TOKEN")
print("Hugging face cache directory from ENV: " + hf_cache_directory)
print("Access token from ENV: " + access_token)

print("Getting tokenizer and model ...")

# get tokenizer and model
tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-2-7b-chat-hf", token=access_token,
                                          cache_dir=hf_cache_directory)
model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-2-7b-chat-hf", torch_dtype=torch.bfloat16,
                                             token=access_token, cache_dir=hf_cache_directory)

start_time = datetime.now()
print("Start time: " + start_time.strftime("%H:%M:%S"))
print("Generating response...")

# create prompt and tokenize it
prompt = ("You will be given the DDL of a table structure. You task is to generate a SQL statement that solves a given task.\
    This is the table structure:" + test_data.SCHEMA + "\
    This is your task: " + test_data.QUESTION)
inputs = tokenizer(prompt, return_tensors="pt")

# generating outputs
outputs = model.generate(**inputs, max_new_tokens=100)
response = tokenizer.decode(outputs[0], skip_special_tokens=True)
print(response)

# calculate and print run statistics
end_time = datetime.now()
print("End time: " + end_time.strftime("%H:%M:%S"))
duration = end_time - start_time
print("Response generation took " + str(duration.total_seconds()) + " seconds")
