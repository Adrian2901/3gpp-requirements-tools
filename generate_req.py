import pandas as pd
import json
import requests

global llm_ip
llm_ip = "localhost:11435"
global llm
llm = "llama3.1"


def ask_llm(paragraph):
    url = f'http://{llm_ip}/api/generate'
    data = {
        "model": llm,
        "prompt": prompts['generate_requirement'] + paragraph,
        "stream": False
        }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=json.dumps(data), headers=headers)
    json_data = json.loads(response.text)
    return json_data['response']

def generate_req(config):
    llm_ip = config['llm_address']
    llm = config['model_name']
    # Read the Paragraph column
    df = pd.read_csv("outputs/latency_paragraphs.csv" , sep=';')
    column = df['Paragraph']
    # ask llm for each row in the column
    print('Generating requirements...')
    for i in range(len(column)):
        paragraph = column[i]
        response = ask_llm(paragraph)
        df.at[i, 'Requirement'] = response
    # Save the new dataframe to a new csv file
    df.to_csv('outputs/new_requirements.csv', sep=';', index=False)
    print('Finished generating requirements!')


with open('prompts.json', 'r') as f:
    prompts = json.load(f)

if __name__ == '__main__':
    generate_req('outputs/latency_paragraphs.csv')






    
