from openai import OpenAI
from datetime import datetime
from csv_logger import write_log
import constants


def run(client, ddl, prompts, dataset_name):
    print('*** Query generation statistics: ***')
    print('Client: ' + client)
    print('Model: ' + 'GPT-4')
    print('Dataset: ' + dataset_name)

    OAClient = OpenAI()

    for i in range(len(prompts)):
        start_time = datetime.now()

        print('Generating response for prompt ' + str(i + 1) + ': ' + prompts[i])

        completion = OAClient.chat.completions.create(
          model="gpt-4-0125-preview",
          messages=[
            {"role": "system", "content": "You will be given the DDL of a table structure. \
            Your task is to generate a SQL statement that solves a given task. \
            Answer with only the SQL Query, nothing else. This is the table structure:" + ddl},
            {"role": "user", "content": "This is your task: " + prompts[i]}
          ]
        )
        
        response = completion.choices[0].message.content

        end_time = datetime.now()
        duration = end_time - start_time

        duration = str(duration.total_seconds())
        print('Elapsed time: ' + duration + ' seconds')
        print('Model response:')
        print(response)
        print('')

        write_log('gpt_4_log.csv', 'a', start_time, client, 'GPT-4', dataset_name, i, prompts[i], duration, response)

    print('Done processing dataset ' + dataset_name + ' on GPT-4')
    print('')
