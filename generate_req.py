import pandas as pd
import json
import requests

global llm_ip
llm_ip = "localhost:11435"
global llm
llm = "llama3.1"


def ask_llm(paragraph, word):
    '''
    Ask the LLM model to generate a requirement.
    :param paragraph: The paragraph to be made into a requirement
    :param word: The word to be used to provide context as part of the prompt
    :return: The response from the LLM model; a generated requirement
    '''



    # Replace {parameter} with the desired term (e.g., "latency"), and setup what we need to send the request (url, data, and headers)
    prompt_text = prompts['generate_requirement'].replace("{parameter}", word) + paragraph
    url = f'http://{llm_ip}/api/generate'
    data = {
        "model": llm,
        "prompt": prompt_text,
        "stream": False
        }
    headers = {'Content-Type': 'application/json'}

    # Send the request to the LLM model, extract the response from the JSON data and return it
    response = requests.post(url, data=json.dumps(data), headers=headers)
    json_data = json.loads(response.text)
    return json_data['response']

def generate_req(config):
    llm_ip = config['llm_address']
    llm = config['model_name']
    word = config['keywords'][0]
    # Read the Paragraph column
    df = pd.read_csv("outputs/latency_paragraphs.csv" , sep=';')
    column = df['Paragraph']
    # ask llm for each row in the column
    print('Generating requirements...')
    for i in range(len(column)):
        paragraph = column[i]
        try:
            response = ask_llm(paragraph, word)
        except Exception as e:
            response = 'Error when generating requirement'
            print(e)
        df.at[i, 'Requirement'] = response
    # Save the new dataframe to a new csv file
    df.to_csv('outputs/new_requirements.csv', sep=';', index=False)
    print('Finished generating requirements!')


with open('prompts.json', 'r') as f:
    prompts = json.load(f)

if __name__ == '__main__':
    generate_req('outputs/latency_paragraphs.csv')






    
