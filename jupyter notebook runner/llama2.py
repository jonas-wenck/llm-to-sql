from datetime import datetime
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from csv_logger import write_log
import constants
import gc

def run(client, ddl, prompts, cache_directory, dataset_name, access_token, additional_context=None):
    print('*** Query generation statistics: ***')
    print('Client: ' + client)
    print('Model: ' + 'Llama 2')
    print('Dataset: ' + dataset_name)

    llama2_model_path = 'meta-llama/Llama-2-7b-chat-hf'

    tokenizer = AutoTokenizer.from_pretrained(llama2_model_path, token=access_token, cache_dir=cache_directory)
    # the system prompt instructs Llama-2 abouts its role and is therefore the same
    system_prompt = ("You will be given the DDL of a table structure of a SQL database. You will also be given a question.\
                     Your task is to generate a SQL query that can be run on the given table structure to answer the given question.\
                     Do not repeat your task in your response. Only include your SQL query in the response.")

    for i in range(len(prompts)):
        start_time = datetime.now()

        additional_context_prompt = f"""                
        This is some additional context about the table structures: {additional_context}
        """
        ddl_and_task = f"""This is the table structure: {ddl} \
        {'' if additional_context is None else additional_context_prompt}
        This is the question: {prompts[i]}
        """

        # this is the desired prompt structure for Llama-2 as described here: https://developer.ibm.com/tutorials/awb-prompt-engineering-llama-2/
        prompt = f"""<s>[INST] <<SYS>>{system_prompt}<</SYS>>{ddl_and_task} [/INST]"""

        print('Generating response for prompt ' + str(i + 1) + ': ' + prompts[i])

        if client == constants.CPU:
            inputs = tokenizer(prompt, return_tensors="pt")
        elif client[:3] == 'gpu':
            inputs = tokenizer(prompt, return_tensors="pt").to("cuda")

        model = load_model(client, llama2_model_path, cache_directory, access_token)

        # Llama-2 always returns the whole prompt in the response, so we need to use a high value for max new tokens
        outputs = model.generate(**inputs, max_length=len(prompt) + 300)
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)

        end_time = datetime.now()
        duration = end_time - start_time

        duration = str(duration.total_seconds())
        print('Elapsed time: ' + duration + ' seconds')
        print('Model response:')
        print(response)
        print('')

        write_log('llama2_log.csv', 'a', start_time, client, 'Llama 2', dataset_name, i, prompts[i], duration, response, False if additional_context is None else True)

        # cleanup
        del model
        gc.collect()
        torch.cuda.empty_cache()

    print('Done processing dataset ' + dataset_name + ' on Llama 2')
    print('')

def load_model(client, model_path, cache_directory, access_token):
    if client == constants.CPU:
        model = AutoModelForCausalLM.from_pretrained(model_path, torch_dtype=torch.bfloat16,
                                                     token=access_token, cache_dir=cache_directory)
    elif client == constants.GPU_3070:
        model = AutoModelForCausalLM.from_pretrained(model_path, torch_dtype=torch.bfloat16,
                                                     token=access_token, cache_dir=cache_directory).to(constants.CUDA)
    elif client == constants.GPU_4090:
        model = AutoModelForCausalLM.from_pretrained(model_path, torch_dtype=torch.bfloat16,
                                                     token=access_token, cache_dir=cache_directory).to(constants.CUDA)
    return model
    
