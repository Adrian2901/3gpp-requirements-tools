import os
import csv
import logging
import argparse
import json
import re
from docx import Document
import requests

# Function to interact with LLM
def ask_llm(paragraph, model_name):
    url = 'http://localhost:11435/api/generate'
    data = {
        "model": model_name,
        "prompt": prompts['verify_context'],
        "stream": False
    }
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.post(url, data=json.dumps(data), headers=headers)
        response.raise_for_status()
        json_data = json.loads(response.text)
        return json_data['response']
    except requests.exceptions.RequestException as e:
        logging.error(f"Error communicating with LLM API: {e}")
        return None

# Function to extract paragraphs with keywords
def extract_paragraphs_with_keywords(doc, keywords, filename, ignored_sections):
    paragraphs = []
    requirements = []
    current_section = ""
    unit_regex = re.compile(rf'\b\d+\s*{re.escape("ms")}\b\.?', re.IGNORECASE)
    requirement_regex = re.compile(r'^\[\w+[\-\.\d]*\]', re.IGNORECASE)
    
    for paragraph in doc.paragraphs:
        if paragraph.style.name.startswith('Heading'):
            current_section = paragraph.text
            continue
        # Check if the paragraph contains any of the keywords
        if any(keyword.lower() in paragraph.text.lower() for keyword in keywords):
            if current_section and not any(ignored in current_section for ignored in ignored_sections):
                paragraphs.append((filename, current_section, paragraph.text))
        # Check if the paragraph contains a requirement or ms unit
        elif unit_regex.search(paragraph.text) or requirement_regex.search(paragraph.text):
            requirements.append((filename, current_section, paragraph.text))
    
    return paragraphs, requirements

# Function to process .docx files
def process_docx_files_in_folder(folder_path, search_word, ignored_sections, output_csv, model_name):
    requirements = []
    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=';')
        csvwriter.writerow(['File', 'Chapter', 'Paragraph', 'LLM response'])
        for filename in os.listdir(folder_path):
            if filename.endswith('.docx'):
                file_path = os.path.join(folder_path, filename)
                logging.info(f"Processing file: {file_path}")
                doc = Document(file_path)
                found_paragraphs, found_requirements = extract_paragraphs_with_keywords(doc, search_word, filename, ignored_sections)
                requirements.extend(found_requirements)
                for filename, section, paragraph in found_paragraphs:
                    llm_response = ask_llm(paragraph, model_name)
                    csvwriter.writerow([filename[:-5], section, paragraph, llm_response])

    logging.info(f"Data written to {output_csv}")

# Main function to set up the CLI
def main():
    parser = argparse.ArgumentParser(description="Process DOCX files and extract paragraphs based on keywords.")
    
    # Command-line arguments
    parser.add_argument('--folder', type=str, default="standards/22_standards", help="The folder path where DOCX files are located.")
    parser.add_argument('--output', type=str, default="outputs/latency_paragraphs.csv", help="The output CSV file for extracted paragraphs.")
    parser.add_argument('--keywords', nargs='+', default=["latency", "latencies"], help="Keywords to search for in the documents.")
    parser.add_argument('--ignored_sections', nargs='+', default=["References", "Appendix", "Definitions", "Abbreviations"], help="Sections to ignore in the documents.")
    parser.add_argument('--model', type=str, default="llama3.1:70b", help="The model to use for LLM.")
    parser.add_argument('--verbose', action='store_true', help="Increase output verbosity (logging).")
    
    args = parser.parse_args()

    # Set logging level based on verbosity
    if args.verbose:
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.WARNING)

    # Load prompts from the JSON file
    with open('prompts.json', 'r') as f:
        global prompts
        prompts = json.load(f)

    # Process the DOCX files with the given arguments
    process_docx_files_in_folder(args.folder, args.keywords, args.ignored_sections, args.output, args.model)

if __name__ == "__main__":
    main()
