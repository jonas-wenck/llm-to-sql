import os


def write_log(fileName, writeType, start_time, client, model, dataset, prompt_index, prompt, duration, response):
    DELIMITER = '^'

    if not os.path.exists(fileName):
        file = open(fileName, 'w')
        file.write(
            'start_time' + DELIMITER + 'client' + DELIMITER + 'model' + DELIMITER + 'dataset' + DELIMITER + 'prompt_id' + DELIMITER + 'prompt' + DELIMITER + 'duration' + DELIMITER + 'response\n')
        file.close()

    prompt_id = dataset + '#' + str(prompt_index + 1)
    file = open(fileName, writeType)
    file.write(str(start_time) + DELIMITER + client + DELIMITER + model + DELIMITER + dataset + DELIMITER + prompt_id + DELIMITER + clean_string(prompt) + DELIMITER + duration + DELIMITER + clean_string(response) + '\n')
    file.close()


def clean_string(string):
    string = string.replace('\n', '')
    string = string.strip()
    return string
