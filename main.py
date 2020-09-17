import re
import requests
import pandas as pd
import os
import csv




def main():
    user_path = os.getcwd()
    input_url = input("Enter the website url: ").strip('http://').strip('https://')
    input_url = f"https://{input_url}"

    if not shouldChangePath(user_path):
        user_path = askNewPath()


    file_name = input ("Input CSV File name (include .csv extension): ")

    full_path = os.path.join(user_path, file_name)

    if not doesFileExist(full_path):
        createCsvFile(full_path)
    

    unique_emails = sendRequest(input_url)

    populateData(full_path, unique_emails)



# checks if we should use the current path returns, returns true or false
def shouldChangePath(user_path):
    while True:
        change_path = input(f"Would you like to keep the current path {user_path} ? (Y/N)").lower()
        if change_path not in ("y","n","yes","no"):
            print("Invalid Input. Please input Yes/No or Y/N.")
            continue
        else: 
            break
    if change_path == "y" or change_path =="yes":
        return True
    else:
        return False


# returns new path
def askNewPath():
    altered_path = input("Enter the desired folder: ")
    return altered_path


# returns true or false based on if the file exists in the given path
def doesFileExist(full_path):
    return os.path.isfile(full_path)
    


# create new excel file
def createCsvFile(full_path):
    open(full_path,"a")


# returns a set of unique emails from target site
def sendRequest(input_url):
    response = requests.get(input_url, verify=False)
    unique_emails = set(re.findall(r"[\w.-]+@[\w.-]+\.\w+", response.text, re.I))
    return unique_emails



# populates data into CSV
def populateData(full_path, unique_emails):
    df = pd.DataFrame(unique_emails)
    df.to_csv(full_path, index=False, mode="a", header=False)
    print(f"Successfully appended {full_path}")



if __name__ == "__main__":
    main()
