from datetime import datetime
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

def llama2_on_cpu(hf_cache_directory, access_token):
    print("hf_cache_directory: " + hf_cache_directory)
    print("access_token: " + access_token)
    print("Getting tokenizer and model ...")

    # get tokenizer and model
    tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-2-7b-chat-hf", token=access_token,
                                              cache_dir=hf_cache_directory)
    model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-2-7b-chat-hf", torch_dtype=torch.float16,
                                                 token=access_token, cache_dir=hf_cache_directory).to("cpu")
    
    start_time = datetime.now()
    print("Start time: " + start_time.strftime("%H:%M:%S"))
    print("Generating response...")

    # create prompt and tokenize it
    prompt = "Transcript of a dialog where the user interacts with an assistant named Bob. Bob is helpful, kind, honest, good at writing and never fails to answer the user's request immediately and with precision. \
              User: Hello, Bob. \
              Bob: Hello. How many I help you today? \
              User: Please tell me the largest city in Europe. \
              Bob: Sure. It is Moscow, the capital of Russia. \
              User: \
              Write a short message to my friend Lukas that I got the model running. Ask him how his day is going. Don't answer further than the message."
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
