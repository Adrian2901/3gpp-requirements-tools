import os
import requests
import json
from docx import Document
from docx.shared import Inches
from docx2python import docx2python
import base64
from PIL import Image
from io import BytesIO, StringIO

def ask_llm(image_path, word):
    '''
    Ask the LLM model to give context to a sequence diagram.
    :param image_path: The path to the image to be analyzed
    :param word: The word to be used to provide context as part of the prompt
    :return: The response from the LLM model; a generated requirement
    '''
    
    # Encode the image to base64 so that it can be sent to the LLM model
    encoded_image = base64.b64encode(open(image_path, "rb").read()).decode('utf-8')

    # Replace {parameter} with the desired term (e.g., "latency"), and setup what we need to send the request (url, data, and headers)
    prompt_text = prompts['generate_image_context'].replace("{parameter}", word) + encoded_image
    url = f'http://localhost:11435/api/generate'
    data = {
        "model": "minicpm-v",
        "prompt": prompt_text,
        "images": [encoded_image],
        "stream": False
        }
    headers = {'Content-Type': 'application/json'}

    # Send the request to the LLM model, extract the response from the JSON data and return it
    response = requests.post(url, data=json.dumps(data), headers=headers)
    json_data = json.loads(response.text)
    return json_data['response']

def extract_images_from_docx(docx_path, output_folder):
    input_doc = docx2python(docx_path, output_folder, html=True)
    output_doc = Document()
    current_section = "No section"

    for line in input_doc.text.splitlines():
        if "<h2>" in line or "<h3>" in line:
            current_section = line
        if "media/image" in line:
            img_name = line[10:].split('-')[0]
            img_path = os.path.join(output_folder, img_name)

            new_name = img_name.replace(".emf", ".png")
            new_path = os.path.join(output_folder, new_name)
            try:
                Image.open(img_path).save(output_folder + "/" + new_name)
                os.remove(img_path)

                output_doc.add_heading(current_section[4:-4], level=1)
                output_doc.add_picture(new_path, width=Inches(6))
                output_doc.add_paragraph(ask_llm(new_path, word="latency"))
                output_doc.add_page_break()
            except Exception as e:
                print(f"Error adding image {img_name} to the document: {e}")

    output_doc.save("diagrams.docx")
                    



def encode_images_to_base64(image_path):
    for img_name in os.listdir(output_folder):
        img_path = os.path.join(output_folder, img_name)
        if img_name.endswith(".emf"):
            
            with open(new_path, "rb") as img_file:
                encoded_string = base64.b64encode(img_file.read()).decode('utf-8')
                print(f"Finished encoding {new_name}.")

                llm_response = ask_llm(encoded_string)

                txt_path = os.path.join(output_folder, f"{new_name[0:-4]}.txt")
                with open(txt_path, "w") as txt_file:
                    txt_file.write(llm_response)

def main():
    standards_folder = "test_files"
    output_folder = "test_images"
    output_file = "extracted_images.docx"
    
    # if not os.path.exists(output_folder):
    #     os.makedirs(output_folder)
    
    # for filename in os.listdir(standards_folder):
    #     if filename.endswith(".docx"):
    #         docx_path = os.path.join(standards_folder, filename)
    #         extract_images_from_docx(docx_path, output_folder)
    #         print(f"Extracted images from {filename}")

    # encode_images_to_base64(output_folder)

    print("Processing images")
    extract_images_from_docx("test_files/23502-i20_l.docx", output_folder)

with open('prompts.json', 'r') as f:
    prompts = json.load(f)


if __name__ == "__main__":
    main()