from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from datetime import datetime
from csv_logger import write_log


def run(client, ddl, prompts, cache_directory, dataset_name):
    print('*** Query generation statistics: ***')
    print('Client: ' + client)
    print('Model: ' + 'Phi-2')
    print('Dataset: ' + dataset_name)

    if client == 'cpu':
        model = AutoModelForCausalLM.from_pretrained("microsoft/phi-2", torch_dtype=torch.float32,
                                                     cache_dir=cache_directory)
    elif client == 'gpu_3070':
        model = AutoModelForCausalLM.from_pretrained("microsoft/phi-2", cache_dir=cache_directory).to("cuda")
    elif client == 'gpu_4090':
        model = AutoModelForCausalLM.from_pretrained("microsoft/phi-2", cache_dir=cache_directory).to("cuda")

    tokenizer = AutoTokenizer.from_pretrained("microsoft/phi-2", cache_dir=cache_directory)

    for i in range(len(prompts)):
        start_time = datetime.now()

        prompt = ("You will be given the DDL of a table structure. Your task is to generate a SQL statement that solves a given task.\
            This is the table structure:" + ddl + "\
            This is your task: " + prompts[i])

        print('Generating response for prompt ' + str(i + 1) + ': ' + prompts[i])

        if client == 'cpu':
            inputs = tokenizer(prompt, return_tensors="pt")
        elif client[:3] == 'gpu':
            inputs = tokenizer(prompt, return_tensors="pt").to("cuda")

        outputs = model.generate(**inputs, max_length=1000)
        response = tokenizer.batch_decode(outputs)[0]

        end_time = datetime.now()
        duration = end_time - start_time

        duration = str(duration.total_seconds())
        print('Elapsed time: ' + duration + ' seconds')
        print('Model response:')
        print(response)
        print('')

        write_log('phi_2_log.csv', 'a', start_time, client, 'Phi-2', dataset_name, i, prompts[i], duration, response)

    print('Done processing dataset ' + dataset_name + ' on Phi-2')
    print('')
