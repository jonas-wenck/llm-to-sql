from datetime import datetime
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from csv_logger import write_log


def run(client, ddl, prompts, cache_directory, dataset_name, access_token):
    print('*** Query generation statistics: ***')
    print('Client: ' + client)
    print('Model: ' + 'Llama 2')
    print('Dataset: ' + dataset_name)

    if client == 'cpu':
        model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-2-7b-chat-hf", torch_dtype=torch.bfloat16,
                                                     token=access_token, cache_dir=cache_directory)
    elif client == 'gpu_3070':
        model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-2-7b-chat-hf", torch_dtype=torch.bfloat16,
                                                     token=access_token, cache_dir=cache_directory).to("cuda")
    elif client == 'gpu_4090':
        model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-2-7b-chat-hf", torch_dtype=torch.bfloat16,
                                                     token=access_token, cache_dir=cache_directory).to("cuda")

    tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-2-7b-chat-hf", token=access_token,
                                              cache_dir=cache_directory)
    for i in range(len(prompts)):
        start_time = datetime.now()

        prompt = ("You will be given the DDL of a table structure. You task is to generate a SQL statement that solves a given task.\
            This is the table structure:" + ddl + "\
            This is your task: " + prompts[i])

        print('Generating response for prompt ' + str(i + 1) + ': ' + prompts[i])

        if client == 'cpu':
            inputs = tokenizer(prompt, return_tensors="pt")
        elif client[:3] == 'gpu':
            inputs = tokenizer(prompt, return_tensors="pt").to("cuda")

        # Llama-2 always returns the whole prompt in the response, so we need to use a high value for max new tokens
        outputs = model.generate(**inputs, max_new_tokens=500)
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)

        end_time = datetime.now()
        duration = end_time - start_time

        duration = str(duration.total_seconds())
        print('Elapsed time: ' + duration + ' seconds')
        print('Model response:')
        print(response)
        print('')

        write_log('llama2_log.csv', 'a', start_time, client, 'Llama 2', dataset_name, i, prompts[i], duration, response)

    print('Done processing dataset ' + dataset_name + ' on Llama 2')
    print('')
