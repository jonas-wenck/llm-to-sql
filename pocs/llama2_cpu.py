from datetime import datetime
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import os
from dotenv import load_dotenv


def llama2_on_cpu():
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
                                                 token=access_token, cache_dir=hf_cache_directory).to("cpu")

    start_time = datetime.now()
    print("Start time: " + start_time.strftime("%H:%M:%S"))
    print("Generating response...")

    # create prompt and tokenize it
    prompt = ("You will be given the DDL of a table structure. You task is to generate a SQL statement that solves a given task.\
        This is the table structure: CREATE TABLE Personnel (\
        StaffID text(9) CONSTRAINT StaffPK PRIMARY KEY,\
        LastName text(15) not null,\
        FirstName text(15) not null,\
        Birthday date,\
        Department text(12) null); \
        This is your task: Find all personal with a birthday after 15.4.1964")
    inputs = tokenizer(prompt, return_tensors="pt").to("cpu")

    # generating outputs
    outputs = model.generate(**inputs, max_new_tokens=100)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    print(response)

    # calculate and print run statistics
    end_time = datetime.now()
    print("End time: " + end_time.strftime("%H:%M:%S"))
    duration = end_time - start_time
    print("Response generation took " + str(duration.total_seconds()) + " seconds")
