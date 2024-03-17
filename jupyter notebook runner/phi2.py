from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from datetime import datetime
from csv_logger import write_log
import constants
import gc


def run(client, ddl, prompts, cache_directory, dataset_name, additional_context=None):
    print('*** Query generation statistics: ***')
    print('Client: ' + client)
    print('Model: ' + 'Phi-2')
    print('Dataset: ' + dataset_name)

    phi2_model_path = 'microsoft/phi-2'

    tokenizer = AutoTokenizer.from_pretrained(phi2_model_path, cache_dir=cache_directory, additional_context=None)

    for i in range(len(prompts)):
        start_time = datetime.now()

        additional_context_prompt = f"""
        This is some additional context about the table structures: {additional_context}\
        """

        prompt = (f"""You will be given the DDL of a table structure. Your task is to generate a SQL statement that solves a given task.\
            This is the table structure: {ddl}\
            {'' if additional_context is None else additional_context_prompt}
            This is your task: {prompts[i]}""")

        print('Generating response for prompt ' + str(i + 1) + ': ' + prompts[i])

        if client == constants.CPU:
            inputs = tokenizer(prompt, return_tensors="pt")
        elif client[:3] == 'gpu':
            inputs = tokenizer(prompt, return_tensors="pt").to(constants.CUDA)

        model = load_model(client, phi2_model_path, cache_directory)

        outputs = model.generate(**inputs, max_length=len(prompt) + 300)
        response = tokenizer.batch_decode(outputs)[0]

        end_time = datetime.now()
        duration = end_time - start_time

        duration = str(duration.total_seconds())
        print('Elapsed time: ' + duration + ' seconds')
        print('Model response:')
        print(response)
        print('')

        write_log('phi_2_log.csv', 'a', start_time, client, 'Phi-2', dataset_name, i, prompts[i], duration, response, False if additional_context is None else True)

        # cleanup
        del model
        gc.collect()
        torch.cuda.empty_cache()

    print('Done processing dataset ' + dataset_name + ' on Phi-2')
    print('')

def load_model(client, model_path, cache_directory):
    if client == constants.CPU:
        model = AutoModelForCausalLM.from_pretrained(model_path, torch_dtype=torch.float32,
                                                     cache_dir=cache_directory)
    elif client == constants.GPU_3070:
        model = AutoModelForCausalLM.from_pretrained(model_path, cache_dir=cache_directory).to(constants.CUDA)
    elif client == constants.GPU_4090:
        model = AutoModelForCausalLM.from_pretrained(model_path, cache_dir=cache_directory).to(constants.CUDA)

    return model