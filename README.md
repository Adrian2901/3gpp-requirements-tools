# Mining 3GPP standards repository for AI-enhanced requirement discovery

<div align="center">
  <table style="border:0px solid white; width:100%;">
    <tr>
      <td align="center" style="border:0px;">
        <img src="https://upload.wikimedia.org/wikipedia/commons/c/c3/Python-logo-notext.svg" alt="Python Logo" width="180">
      </td>
      <td align="center" style="border:0px;">
        <img src="https://api.nuget.org/v3-flatcontainer/ollamasharp/3.0.14/icon" alt="Ollam Logo" width="180" height="">
      </td>
      <td align="center" style="border:0px;">
        <img src="https://raw.githubusercontent.com/OpenBMB/MiniCPM-V/refs/heads/main/assets/minicpmv.png" alt="Mini-cpm Logo" width="180">
      </td>
    </tr>
  </table>
</div>

## :book: Table of Contents
- [About the project](#about-the-project)
- [Solution Architecture](#solution-architecture)
- [How to use](#how-to-use)
- [Authors](#authors)
- [License](#license)

## :bulb: About the project
In this project we aimed to use the assisstance of the Large-language-Models(LLMs) in order to extract useful requirements from 3GPP standards.
With advances in generative AI and large language models (LLMs), we can now leverage these tools to automate the extraction of requirements from complex technical documents. Traditionally, requirements elicitation from dense standards like 3GPP has been time-consuming and requires lot of manual work. This project aims to address these challenges by using LLMs to streamline the extraction process, reducing manual effort, improving accuracy, and making the process more efficient and reliable.

Tech stack used in the project: 
* Ollama 
* Mini-cpm
* Python

## :triangular_ruler: Solution Architecture

<img src="./diagrams-and-pictures/blue_divider_transparent.png" alt="Divider" style="width: 100%; display: block;">

![Diagram](/diagrams-and-pictures/architecture.png)
<img src="./diagrams-and-pictures/blue_divider_transparent.png" alt="Divider" style="width: 100%; display: block;">



The architecture diagram illustrates a pipeline for automating the extraction and generation of requirements from 3GPP standards using Python scripts and LLMs, with human oversight to ensure accuracy. It begins with the retriever, a Python script that downloads the standards from the 3GPP repository in .docx format, unzipping them into a local folder. The next step involves filtering paragraphs containing specific keywords (e.g., "capacity") to identify relevant sections for requirements elicitation. These filtered paragraphs are fed into the LLM (Llama 3.1), which categorizes them as either applicable or non-applicable for generating requirements. Non-applicable paragraphs are stored in a CSV file for later review, while the applicable ones are passed through the same LLM to generate requirement-like text. The generated requirements are paired with their corresponding original paragraphs for traceability and are outputted alongside the non-applicable paragraphs in a formatted Excel file. This ensures that the requirements engineer can evaluate the results, reviewing non-applicable paragraphs to detect possible AI hallucinations and validating the generated requirements for accuracy. The process is designed to balance automation with human supervision, enabling efficient yet reliable requirements extraction.

## :wrench: How to use
**Donwload standards tab**
<img src="./diagrams-and-pictures/blue_divider_transparent.png" alt="Divider" style="width: 100%; display: block;">


![download-standards-tab](/diagrams-and-pictures/sc-retriever-edited.PNG)

<img src="./diagrams-and-pictures/blue_divider_transparent.png" alt="Divider" style="width: 100%; display: block;">

1. Specify the 3GPP standard series you wish to download.  
   (**Note:** Leaving the input blank will download all series.)

2. Enter a keyword to search for in the titles of the standards.

3. Choose whether to include or exclude technical reports or technical specifications.

4. Specify the folder path where the standards should be downloaded.

5. Click "Download" and wait for all the standards to be downloaded.

**Generate requirements tab**
<img src="./diagrams-and-pictures/blue_divider_transparent.png" alt="Divider" style="width: 100%; display: block;">

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

## :busts_in_silhouette: Authors

## :scroll: License



<style>
table {
    border-collapse: collapse;
}
table, th, td {
   border: none;
}
blockquote {
    border-left: none;
    padding-left: 10px;
}
</style>