"""
File: generate_req.py
Description: This script generates requirements by asking a generative AI to create a requirement for
each paragraph where a given keyword is found.

Contributors:
Marcelo Santibáñez
David Schön
Adrian Hassa

Created: 2024-10-11
Last Modified: 2024-12-10

Project: 3GPP Requirement Tools
URL: https://github.com/Adrian2901/3gpp-requirements-tools

License: MIT License (see LICENSE file for details)
"""

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

def generate_req(config, update):
    ''' 
    Generate requirements from a list of paragraphs containing keywords.
    :param config: The configuration dictionary
    :param update: The function to update the GUI status and progress bar
    '''
    llm_ip = config['llm_address']
    llm = config['model_name']

    word = config['keywords'][0]
    latency_paragraphs = config["output_folder_path"] + "/possible_paragraphs.csv"
    output_csv = config["output_folder_path"] + "/new_requirements.csv"
    # Read the Paragraph column
    df = pd.read_csv(latency_paragraphs , sep=';')
    column = df['Paragraph']
    # ask llm for each row in the column
    for i in range(len(column)):
        update('Generating requirements...', i/len(column))
        paragraph = column[i]
        try:
            response = ask_llm(paragraph, word)
        except Exception as e:
            response = 'Error when generating requirement'
            print(e)
        df.at[i, 'Requirement'] = response
    # Save the new dataframe to a new csv file
    df.to_csv(output_csv, sep=';', index=False)
    update('Finished generating requirements!')

with open('prompts.json', 'r') as f:
    prompts = json.load(f)

if __name__ == '__main__':
    print("This is a script that takes 3GPP standards and converts them into LLM-generated requirements.\nUsage: python gui_requirements.py")