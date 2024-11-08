"""
The csv2xlsx converter processes all the generated CSV files and converts them into a single XLSX file. It also highlights
the keyword in the paragraph and requirement columns. The output XLSX file will have three sheets: new_requirements,
 latency_paragraphs, and latency_no_paragraphs.
"""

import csv
import xlsxwriter
import re

def highlight_keyword(paragraph, keyword, sheet, row_idx, bold_format, wrap_format):
    matches = list(re.finditer(f'({keyword})', paragraph, flags=re.IGNORECASE))  # Use finditer for all matches
    rich_text = []
    start_index = 0
    for match in matches: # Logic of this loop comes from CHAT-GPT
        # Add the text before the match
        if match.start() > start_index:
            rich_text.append(paragraph[start_index:match.start()])  # Normal text
                    # Append the matched keyword with bold format
            rich_text.append(bold_format)  # Bold format for keyword
            rich_text.append(match.group(0))  # The actual keyword
            start_index = match.end()  # Update start_index to end of match

                # Add any remaining text after the last match
            if start_index < len(paragraph):
                rich_text.append(paragraph[start_index:])  # Normal text
                # Write the rich text back to the 'Paragraph' cell with wrapping
            if rich_text:
                sheet.write_rich_string(row_idx, 2, *rich_text)  # Column 2: Paragraph
            else:
                # Write paragraph normally with wrapping if the keyword is not found
                sheet.write(row_idx, 2, paragraph, wrap_format)
            # sheet.set_row(row_idx, None, wrap_format)  # Enable text wrapping for the entire row

# Defautl input_csv is a list of the three csv files containing the default names we used in the project
def csv_to_xlsx(config):
    keyword = config['keywords'][0] # keyword to highlight TODO: iterate thru the list of keywords
    latency_possible = config['latency_possible']
    latency_no = config['latency_no']
    new_requirements = config['new_requirements']
    output_xlsx = config['output_xlsx']  #output xlsx file

     #input csv files(not specified in config for now)
    print("Processing CSV to XLSX...")

    print(latency_possible)
    print(latency_no)
    print(new_requirements)

    # different input files
    # 1 and 2 have the same structure so different logic is only needed for 0


    # Create a new XLSX file
    workbook = xlsxwriter.Workbook(output_xlsx) 
    # Add a format for the header cells
    header_format = workbook.add_format({'bold': True, 'align': 'center', 'valign': 'vcenter', 'fg_color': '#D7E4BC'})
    # wrap text
    wrap_format = workbook.add_format({'text_wrap': True, 'valign': 'top'})
    # bold format for the keyword
    bold_format = workbook.add_format({'bold': True})

    # Create a sheet for each input file
    workbook.add_worksheet("new_requirements")
    workbook.add_worksheet("latency_possible_paragraphs")
    workbook.add_worksheet("latency_no_paragraphs")

    # Create columns for the sheets
    for sheet in workbook.worksheets():
        sheet.write_row(0, 0, ["File", "Chapter", "Paragraph", "LLM Response"], header_format) # headers
        sheet.set_column('A:A', 10)  # File column
        sheet.set_column('B:B', 18)  # Chapter column
        sheet.set_column('C:C', 45, wrap_format)  # Paragraph column
        sheet.set_column('D:D', 10)  # LLM Response column
        if sheet.get_name() == "new_requirements":
            sheet.write(0, 4, "Requirement", header_format) # Requirement column
            sheet.set_column('E:E', 45)  # Requirement column

 

    # read new_requirements.csv and write to its sheet
    with open(new_requirements, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=';')
        for row in reader:
            file, chapter, paragraph, llm_response, requirement = row
            sheet = workbook.get_worksheet_by_name("new_requirements") # Get the sheet
            row_idx = sheet.dim_rowmax + 1 # Get the next available row (after the header)
            sheet.write(row_idx, 0, file)         # Column 0: File
            sheet.write(row_idx, 1, chapter)      # Column 1: Chapter
            sheet.write(row_idx, 2, paragraph, wrap_format)    # Column 2: Paragraph
            sheet.write(row_idx, 3, llm_response) # Column 3: LLM Response
            sheet.write(row_idx, 4, requirement, wrap_format) # Column 4: Requirement
             # Check if the keyword is in the paragraph and highlight it
            highlight_keyword(paragraph, keyword, sheet, row_idx, bold_format, wrap_format)
            # highlight keyword for the requirement column 
            highlight_keyword(requirement, keyword, sheet, row_idx, bold_format, wrap_format)
           
    
    # read latency_possible.csv and write to its sheet
    with open(latency_possible, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=';')
        for row in reader:
            file, chapter, paragraph, llm_response = row
            sheet = workbook.get_worksheet_by_name("latency_possible_paragraphs")
            row_idx = sheet.dim_rowmax + 1 # Get the next available row (after the header)
            sheet.write(row_idx, 0, file)         # Column 0: File
            sheet.write(row_idx, 1, chapter)      # Column 1: Chapter
            sheet.write(row_idx, 2, paragraph, wrap_format)     # Column 2: Paragraph
            sheet.write(row_idx, 3, llm_response) # Column 3: LLM Response
            # Check if the keyword is in the paragraph and highlight it
            highlight_keyword(paragraph, keyword, sheet, row_idx, bold_format, wrap_format)

    # read latency_no.csv and write to its sheet
    with open(latency_no, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=';')
        for row in reader:
            file, chapter, paragraph, llm_response = row
            sheet = workbook.get_worksheet_by_name("latency_no_paragraphs")   
            row_idx = sheet.dim_rowmax + 1 # Get the next available row (after the header)     
            sheet.write(row_idx, 0, file)         # Column 0: File
            sheet.write(row_idx, 1, chapter)      # Column 1: Chapter
            sheet.write(row_idx, 2, paragraph, wrap_format)     # Column 2: Paragraph
            sheet.write(row_idx, 3, llm_response) # Column 3: LLM Response
            # Check if the keyword is in the paragraph and highlight it
            highlight_keyword(paragraph, keyword, sheet, row_idx, bold_format, wrap_format)

    #close the workbook
    workbook.close()
    print(f"Conversion complete! Output saved to {output_xlsx} ")
   


# Example usage
# outputs = ['outputs\\new_requirements.csv', "outputs\latency_paragraphs.csv", "outputs\latency_no_paragraphs.csv"]

# csv_to_xlsx(outputs, "outputs\output.xlsx", "latency")


