import os
import re
from bs4 import BeautifulSoup

def sanitize_filename(title):
    # Define a pattern for invalid characters (for most filesystems)
    invalid_chars = r'[<>:"/\\|?*]'

    # Replace invalid characters with an underscore
    sanitized_title = re.sub(invalid_chars, '_', title)

    # Optionally, you can strip leading/trailing spaces
    sanitized_title = sanitized_title.strip()

    return sanitized_title

def file_directory():

    current_directory = os.path.dirname(os.path.abspath(__file__))

    folder_path = os.path.join(current_directory, 'brave_search_article')

    return folder_path


def create_directory_if_not_exists(directory_path):
    # Check if the directory exists
    if not os.path.exists(directory_path):
        # Create the directory
        os.makedirs(directory_path)
        # print(f"Directory '{directory_path}' created successfully.")
    else:
        print(f"Directory '{directory_path}' already exists.")

    return

def write_content_to_html(title, response, ollama_result, today_date, now, page_url):

    folder_path = file_directory()

    soup = BeautifulSoup(response.text, 'html.parser')

    html_web_content = soup.prettify()

    #ollama response content

    #html_content = f"<html><body><p>{title} <br> {ollama_result.replace('\n', '</p><p>')}</p></body></html>"
    html_content = f"<html><body><p>{title} <br> {ollama_result.replace('\n', '<br>')}</p></body></html>"

    html_reference = f"<p>Reference: <a href=\"{page_url}\" target=\"_blank\">{page_url}</a></p>"

    file_content = str(html_content) + str(html_reference)


    sanitized_title = sanitize_filename(title)

    filename = str(sanitized_title) + ".html"

    outputfiledirectory = str(folder_path) + "\\" + str(today_date)
    create_directory_if_not_exists(outputfiledirectory)

    outputfilename_webpage = str(folder_path) + "\\" + str(today_date) + "\\" + \
                     str(sanitized_title) + ".html"

    outputfilename_ollama_response = str(folder_path) + "\\" + str(today_date) + "\\" + \
                             str(sanitized_title) + "_w_ollama_response.html"


    # Save webpage content to file
    with open(outputfilename_webpage, 'w', encoding='utf-8') as file:
        file.write(html_web_content)

        print(f'Webpage saved to {outputfilename_webpage}')

    # Save ollama response to file
    with open(outputfilename_ollama_response, 'w', encoding='utf-8') as file:
        file.write(file_content)

        print(f'Webpage saved to {outputfilename_ollama_response}')

    return