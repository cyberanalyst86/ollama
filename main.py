import requests
import json
import pandas as pd
import os
import time
from datetime import datetime
from brave_browser_search import *
from ollama_prompt import *

#----------------Brave browser search query parameters----------------#
#q = brave search query term
q = "Veeva Systems Inc"

"""The maximum is 20. The actual number delivered may be less than requested.
Combine this parameter with offset to paginate search results.
count = brave number of search results per page"""
count = 20

#Get result from 1st page to 10th page
#offset = brave_up_to_page
offset = 1

"""The following values are supported: - pd:
Discovered within the last 24 hours. - pw:
Discovered within the last 7 Days. - pm:
Discovered within the last 31 Days. - py:
Discovered within the last 365 Days… - YYYY-MM-DDtoYYYY-MM-DD:
timeframe is also supported by specifying the date range e.g. 2022-04-01to2022-07-30"""
#freshness = brave search filter by duration
freshness = "pm"

#----------------------------------------------------------------------#

def get_today_date():

    today_date = datetime.today().date()

    return today_date

def get_now():

    now = datetime.now()

    formatted_now = now.strftime('%Y-%m-%d %H-%M-%S')

    return formatted_now

def file_directory():

    current_directory = os.path.dirname(os.path.abspath(__file__))

    folder_path = os.path.join(current_directory, 'brave_search_result')

    return folder_path

import os

def create_directory_if_not_exists(directory_path):
    # Check if the directory exists
    if not os.path.exists(directory_path):
        # Create the directory
        os.makedirs(directory_path)
        #print(f"Directory '{directory_path}' created successfully.")
    else:
        print(f"Directory '{directory_path}' already exists.")

    return


def main():

    folder_path = file_directory()
    now = get_now()

    outputfiledirectory = str(folder_path) + "\\" + str(get_today_date())
    create_directory_if_not_exists(outputfiledirectory)

    #----Define outputfilename for brave search result in excel----
    outputfilename = str(folder_path) + "\\" + str(get_today_date()) + "\\" + str(now) + "_" + \
    str(q) + ".xlsx"

    #----Call brave search function----
    print("Query Brave......")
    df_brave_search_result = brave_search(q, count, offset, freshness)

    #----Write brave search result in dataframe to excel
    print("Write to search result to excel ......\n")
    df_brave_search_result.to_excel(outputfilename, index=False)


    ollama_result_list = []

    #----Call Ollama prompt function----

    for index, row in df_brave_search_result.iterrows():

        start_time = time.time()

        ollama_result = ollama_prompt(row["url"], row["title"], get_today_date(), now)

        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Elapsed time for ollama prompt: {elapsed_time:.2f} seconds")

        ollama_result_list.append(ollama_result)

    df_brave_search_result["ollama result"] = ollama_result_list

    outputfilename = str(folder_path) + "\\" + str(get_today_date()) + "\\" + str(now) + "_" + \
                     str(q) + "_w_ollama_results.xlsx"


    print("Write search result with ollama prompt response to excel ......\n")

    df_brave_search_result.to_excel(outputfilename, index=False)

    print("Operation completed !!!")
    
if __name__ == "__main__":

    main()