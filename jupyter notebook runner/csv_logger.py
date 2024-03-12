import os

def write_log(fileName, writeType, client, model, dataset, prompt, time, response):
    DELIMITER = '^'

    if not os.path.exists(fileName):
        file = open(fileName, 'w')
        file.write('client' + DELIMITER + 'model' + DELIMITER + 'dataset' + DELIMITER + 'prompt' + DELIMITER + 'time' + DELIMITER + 'response\n')
        file.close()
    
    file = open(fileName, writeType)
    file.write(client + DELIMITER + model + DELIMITER + dataset + DELIMITER + clean_string(prompt) + DELIMITER + time + DELIMITER + clean_string(response) + '\n')
    file.close()


def clean_string(string):
    string = string.replace('\n', '')
    string = string.strip()
    return string