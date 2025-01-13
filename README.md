# 3GPP Requirement Tools


## 📕 Table of Contents
- [About the project](#about-the-project)
- [Solution Architecture](#solution-architecture)
- [How to use](#how-to-use)
- [Setup](#setup)
- [Authors](#authors)

## 💡About the project
In this project we aimed to use the assisstance of the Large-language-Models(LLMs) in order to extract useful requirements from 3GPP standards.
With advances in generative AI and large language models (LLMs), we can now leverage these tools to automate the extraction of requirements from complex technical documents. Traditionally, requirements elicitation from dense standards like 3GPP has been time-consuming and requires lot of manual work. This project aims to address these challenges by using LLMs to streamline the extraction process, reducing manual effort, improving accuracy, and making the process more efficient and reliable.

Tech stack used in the project: 
* [Python](https://www.python.org/)
* [Ollama](https://github.com/ollama/ollama)

This repository was migrated from [miroslawstaron/requirements_standards](https://github.com/miroslawstaron/requirements_standards)

## 📐Solution Architecture

<img src="./diagrams-and-pictures/blue_divider_transparent.png" alt="Divider" style="width: 100%; display: block;">

![Diagram](/diagrams-and-pictures/architecture.png)
<img src="./diagrams-and-pictures/blue_divider_transparent.png" alt="Divider" style="width: 100%; display: block;">



The architecture diagram illustrates a pipeline for automating the extraction and generation of requirements from 3GPP standards using Python scripts and LLMs, with human oversight to ensure accuracy. It begins with the retriever, a Python script that downloads the standards from the 3GPP repository in .docx format, unzipping them into a local folder. The next step involves filtering paragraphs containing specific keywords (e.g., "capacity") to identify relevant sections for requirements elicitation. These filtered paragraphs are fed into the LLM (Llama 3.1), which categorizes them as either applicable or non-applicable for generating requirements. Non-applicable paragraphs are stored in a CSV file for later review, while the applicable ones are passed through the same LLM to generate requirement-like text. The generated requirements are paired with their corresponding original paragraphs for traceability and are outputted alongside the non-applicable paragraphs in a formatted Excel file. This ensures that the requirements engineer can evaluate the results, reviewing non-applicable paragraphs to detect possible AI hallucinations and validating the generated requirements for accuracy. The process is designed to balance automation with human supervision, enabling efficient yet reliable requirements extraction.

## Setup

For certain functionality to work one needs to setup a locally running LLM model. This setup is necessary as following:
- Standards Retriever: No Setup
- Sequence Diagram Retriever: Optional
- Requirements Generator: Mandatory

Script setup guide:
1. Download and install Python 3.8+
2. Navigate to the project folder and run `pip install -r requirements.txt` in the terminal to install dependencies
3. Run the `main.py` script to open a window containing all tools

You can find executable files, which don't require any dependecies, on the [Releases page](https://github.com/Adrian2901/3gpp-requirements-tools/releases). 

## 🔧How to use

<img src="./diagrams-and-pictures/blue_divider_transparent.png" alt="Divider" style="width: 100%; display: block;">

**Donwload standards tab**

![download-standards-tab](/diagrams-and-pictures/sc-retriever-edited.PNG)

<img src="./diagrams-and-pictures/blue_divider_transparent.png" alt="Divider" style="width: 100%; display: block;">

1. Specify the 3GPP standard series you wish to download.  
   (**Note:** Leaving the input blank will download all series.)

2. Enter a keyword to search for in the titles of the standards.

3. Choose whether to include or exclude technical reports or technical specifications.

4. Specify the folder path where the standards should be downloaded.

5. Click "Download" and wait for all the standards to be downloaded.


<img src="./diagrams-and-pictures/blue_divider_transparent.png" alt="Divider" style="width: 100%; display: block;">

**Generate requirements tab**

![Generate-requirements-tab](/diagrams-and-pictures/sc-genreq-edited.PNG)

<img src="./diagrams-and-pictures/blue_divider_transparent.png" alt="Divider" style="width: 100%; display: block;">

6. Specify the LLM address and port.  
   You can use an LLM running on your local host or provide the address of an external one.

7. Select the LLM you wish to use for requirements elicitation.

8. Choose the folder path containing the standard files.  
   *(This could be the folder specified for downloading standards in step 4.)*

9. Specify the output folder where the Excel sheets with extracted requirements will be saved.

10. Enter the keywords to be used for eliciting requirements.

11. Select the units of measurement for the keyword, if applicable.

12. Click "Run" and wait for the process to complete.  
    Once finished, check the output folder for the results.

## 👥Authors

Adrian Hassa: [@Adrian2901](https://github.com/Adrian2901)

Amirpooya Asadollahnejad: [@amirpooya78](https://github.com/amirpooya78)

David Schön: [@DavinciOfSweden](https://github.com/DavinciOfSweden)

Marcelo Santibáñez: [@ssheloors](https://github.com/ssheloors)
