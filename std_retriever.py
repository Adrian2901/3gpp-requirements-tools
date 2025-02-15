"""
File: std_retriever.py
Description: This script connects to the 3GPP FTP server to download specified standard
files and stores them in the designated 'standards' folder.

Contributors:
Amirpooya Asadollahnejad
David Schön
Marcelo Santibáñez
Adrian Hassa

Created: 2024-10-12
Last Modified: 2024-12-10

Project: 3GPP Requirement Tools
URL: https://github.com/Adrian2901/3gpp-requirements-tools

License: MIT License (see LICENSE file for details)
"""

from ftplib import FTP, error_perm
import json
import re
import os
import zipfile
import pandas as pd 
import shutil
import sys

# Change the working directory to the directory of the executable for PyInstaller
os.chdir(sys._MEIPASS) if getattr(sys, 'frozen', False) else os.chdir(os.path.dirname(os.path.abspath(__file__)))
##############################################
# Configuration variables
host = "www.3gpp.org"
ftp_directory_path = "Specs/archive"
download_folder_path = "zipped_standards"
excel_spec_file = "Specification_list.xlsx"
standard_specs_folder_path = "standard_specs_folder"

##############################################

class FTPClient:
    def __init__(self, host, user='', passwd=''):
        self.host = host
        self.ftp = FTP(host)  # Establish connection upon initialization
        try:
            self.ftp.login(user=user, passwd=passwd)
            print(f"Logged in to {self.host}")
        except Exception as e:
            print(f"Error connecting to {self.host}: {e}")
            raise

    def change_directory(self, path):
        """Change the working directory on the FTP server."""
        try:
            self.ftp.cwd(path)
            print(f"Changed to directory: {self.ftp.pwd()}")
        except error_perm as e:
            print(f"Permission error changing directory: {e}")
            raise
        except Exception as e:
            print(f"Error changing directory: {e}")
            raise
    
    def list_directory(self):
        dir_content = []
        try:
            self.ftp.retrlines('LIST', lambda line: dir_content.append(line))
        except Exception as e:
            print(f"Error listing directory: {e}")
            raise
        return dir_content

    def download(self, filename, local_path):

        # Ensure that `local_path` is a directory, and construct the full path to the file
        full_path = os.path.join(local_path, filename)
        with open (full_path, 'wb') as file:
            try:
                self.ftp.retrbinary(f'RETR {filename}', file.write)
                print(f"Downloaded {filename} to {local_path}")
            except Exception as e:
                print(f"An Error occured while downloading {filename} to {local_path}")
                #print(e)

    def close_connection(self):
        if self.ftp:
            self.ftp.close()
            print(f"Disconnected from {self.host}")

# std_list is path to the JSON file that contains the name of the files alongside their version
# local_path is path to the destination folder you want to download standards to
def get_standards(ftp_client: FTPClient, std_list: str, local_path: str, update):
    os.makedirs(local_path, exist_ok=True) # creating a directory if it does not exist.
    #clear_folder(local_path)
    #open the json file
    with open(std_list, 'r') as series_list:
        series_data = json.load(series_list) # load the data from json file 
        series_found = False

        # check if a directory with given number exists 
        for entry in ftp_client.list_directory():
            if(series_data["series_no"] + "_series" in entry):
                ftp_client.change_directory(series_data["series_no"] + "_series")
                series_found = True
                break
        
        # Terminate the process if given series was not found
        if(not series_found):
            print(f'{series_data["series_no"]} was not found.')
            update(f'{series_data["series_no"]} was not found.')
            return
        
        # search for the given files in the series folder
        for entry in ftp_client.list_directory():
            for index in series_data['indexes']: 
                if(series_data['series_no'] + "."+ index['spec_no'] in entry):
                    try:
                        ftp_client.change_directory(series_data['series_no'] + "." + index['spec_no']) # change directory to the current standard folder
                    except Exception as e:
                        print(f"Error changing directory to {series_data['series_no'] + '.' + index['spec_no']}: {e}")
                        continue
                    # check for the version that needs to be downloaded
                    if(index['version'] == 'latest'):
                        all_versions = ftp_client.list_directory()
                        if(len(all_versions) == 0):
                            ftp_client.change_directory('..')
                            continue
                        last_entry: str = all_versions[-1] # since in the 3Gpp files are organized by date latest is always the last entry of the directory
                        filename_ = last_entry.split()[-1] # Extract the name of the file from the entry
                        ftp_client.download(filename_, local_path)
                    else:
                        filename_ = series_data['series_no'] + index['spec_no'] + '-' + index['version'] + ".zip"
                        ftp_client.download(filename_, local_path)
                    update("Downloading " + filename_)
                    
                    ftp_client.change_directory('..') # going back one directory up after being finished with the current file 
        
        # getting back to the original path after downloading all the standards 
        if(ftp_client.ftp.pwd() != ftp_directory_path):
            ftp_client.change_directory('..')
            
def unzip_all_in_folder(folder_path, extract_to): # This function is created by Chat-GPT
    os.makedirs(extract_to, exist_ok=True)
    clear_folder(extract_to)
    # List all files in the folder
    for file_name in os.listdir(folder_path):
        # Construct full file path
        file_path = os.path.join(folder_path, file_name)
        
        # Check if it's a valid zip file
        if zipfile.is_zipfile(file_path):
            print(f'Unzipping {file_name}...')
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                # Extract the files to the destination folder
                zip_ref.extractall(extract_to)

            # removing the zipped file after it is unzipped to the 'extract_to' path 
            os.remove(file_path)
        else:
            print(f'Skipping {file_name}, not a zip file.')

def search_title(folder_path, xlsx_file, config): # folder_path: where json files will be stored, xlsx_file: excel file thatt holds the spec_no s and titles.
    os.makedirs(folder_path, exist_ok=True)
    clear_folder(folder_path)

    phrase = config["phrase"]
    series_no = config["series_no"]
    lookedup_publicitation = config["publication"]
    lookedup_technology = config["technology"]
    lookedup_status = config["status"]
    lookedup_specification_number = config["specification_number"]
    lookedup_type = config["type"]

    # If a phrase is provided, create a regular expression based on it; otherwise, match all titles
    pattern = re.compile(phrase, re.IGNORECASE) if phrase else None

    df = pd.read_excel(xlsx_file) # read xlsx file 

    previous_series = ""
    data = {} # for creating json file for each series 

    # Mapping of keywords to columns from the Excel file
    keyword_column_map = {
        "Publication": lookedup_publicitation,
        "Status": lookedup_status,
        "Technology": lookedup_technology,
        "Spec No": lookedup_specification_number,
        "Type": lookedup_type
    }

    # Function to check if a row matches the keyword criteria
    def row_matches(row):
        for column, keyword in keyword_column_map.items():
            if isinstance(keyword, list):  # check if the keyword is a list
                if not any(item in str(row[column]) for item in keyword): # check if any of the items in the list is in the column
                    return False
            elif keyword not in str(row[column]):  # if not in the list, check if the keyword is in the column
                return False
        return True # if all the criteria are met return True

    # Apply the mapping function to the dataframe
    result = df[df.apply(row_matches, axis=1)]

    # going through each row of excel file 
    for index, row in result.iterrows():
        current_spec:str = row["Spec No"]
        title:str = row["Title"]

        current_series = current_spec.split('.')[0]

        if (series_no and current_series != series_no): # If a series number is specified and it does not match the current series number we don't save the specifications
            continue        

        if(current_series != previous_series): # Then save data of previous series to a json file and reset the data
            if(previous_series): # since when we start at first there is no previous series
                json_filename = os.path.join(folder_path, f"{previous_series}_series.json")
                with open(json_filename, 'w') as json_file:
                    json.dump(data, json_file, indent=4)
            
            # Reset data
            data = { 
                "series_no": current_series,
                "indexes": []
            }
        
        if pattern:
            if pattern.search(title): # search for the phrase in title 
                data['indexes'].append({
                    "spec_no": current_spec.split('.')[1],
                    "version": "latest"
                })
        else:  # If no phrase, match all titles
            data['indexes'].append({
                    "spec_no": current_spec.split('.')[1],
                    "version": "latest"
                })
        
        previous_series = current_series # update the previous series

    # Save the last series data if needed
    if data['indexes']:
        json_filename = os.path.join(folder_path, f"{previous_series}_series.json")
        with open(json_filename, 'w') as json_file:
            json.dump(data, json_file, indent=4)
    
    file_names = []
    # Iterate over files in the folder
    for file_name in os.listdir(folder_path):
    # Check if it's a file (to exclude directories)
        if os.path.isfile(os.path.join(folder_path, file_name)):
            file_names.append(file_name)
    # return the name of created json files that specific phrase was found in their title
    return file_names 
        
def clear_folder(folder_path): # This function is created by Chat-GPT
    # Check if the folder exists
    if os.path.exists(folder_path):
        # Check if the folder is empty
        if not os.listdir(folder_path):  # `os.listdir` returns an empty list if the folder is empty
            print("Folder is empty.")
        else:
            # Folder is not empty; delete its contents
            for filename in os.listdir(folder_path):
                file_path = os.path.join(folder_path, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)  # Remove the file
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)  # Remove the directory
                    print(f"Deleted: {file_path}")
                except Exception as e:
                    print(f"Failed to delete {file_path}. Reason: {e}")
            print("Folder contents cleared.")
    else:
        print("Folder does not exist.")

#################### script #########################

def download(config, button_handler, update):
    button_handler.config(state="disabled")
    unzipped_folder_path = config["download_folder_path"] 
    phrase = config["phrase"]
    series_no = config["series_no"]

    try:
        # create the connection to FTP server and change to the wanted directory
        ftp_client = FTPClient(host)
        ftp_client.change_directory(ftp_directory_path)

        #* search by title if necessary
        standards = search_title(standard_specs_folder_path, excel_spec_file, config)

        for standard in standards:
            get_standards(ftp_client, os.path.join(standard_specs_folder_path, standard) , download_folder_path, update)

        # unzip the downloaded standards 
        update("Unzipping downloaded standards...")
        unzip_all_in_folder(download_folder_path, unzipped_folder_path)

        # removing the standards_specs folder
        update("Cleaning up...")
        shutil.rmtree(standard_specs_folder_path)

        update("Done! Check the output folder for the results.")
    except Exception as e:
        update(f"An error occured: {e}. Please try again.")
    finally:
        ftp_client.close_connection()
        button_handler.config(state="normal")


if __name__ == "__main__":
    print("This is a script that retrieves 3GPP standards documents with filters.\nUsage: python gui_std_retriever.py")