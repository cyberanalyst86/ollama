import asyncio
from langchain_community.document_loaders import WebBaseLoader
import ollama
from bs4 import BeautifulSoup
import requests
from write_article_to_html import *

def ollama_prompt(page_url, title, today_date, now):

    response_web = requests.get(page_url)

    if response_web.status_code == 200:

        loader = WebBaseLoader(web_paths=[page_url])
        docs = []

        print("performing ollama prompt......")
        print(f"Article Title: {title}")
        print("###############################################################################")

        async def async_function():
            async for doc in loader.alazy_load():
                docs.append(doc)

        # Run the async function
        asyncio.run(async_function())
        doc = docs[0]
        passage = doc.page_content


        #print(f"Article content: \n {doc.page_content}")
        #print("----------------------------------------------------------------------------")

        #prompt = "help to summarize the following passage and convert into html format for easy reading"
        #prompt = "Tell me about \"APT41's aliases\", \"motivation of attack\"," \
        #"\"malwares use\", \"tools used\", \"vulnerabilities exploited\", " \
        #"\"targeted industry\", \"targeted region or country\" , \"tactic, technique and procedures\", " \
        #"\"Mitre Att&ck tactics and techniques\", \"indicators of compromise\", " \
        #"\"key information to take away\" from the following write up and then convert into html format for easy reading: \""

        #prompt = "What is the core idea about generative artificial intelligence for me to take away from the following and provide me the evidence which you use to conclude this: \""

        prompt = "help to summarize the following passage and convert into html format for easy reading: \""

        content = str(prompt) + str(passage) + "\""

        response = ollama.chat(
            model="llama3:8b",
            messages=[
                {
                    "role": "user",
                    "content": content,
                },
            ],
        )

        ollama_result = response["message"]["content"]
        print(f"ollama result: \n {ollama_result}")
        print("_____________________________________________________________________________\n")

        print("Writing content to html......")
        print("_____________________________________________________________________________\n")

        #content_title = f"<p>Title: {title}<br></p>"
        #content_url = f"<p>Reference: <a href=\"{page_url}\">{page_url}<br></a></p>"
        #content_article = str(passage) + "\n"
        #content_ollama_result = ollama_result

        #content = str(content_title) + "\n" + str(content_url) + "\n" + str(content_article) + "\n" + \
        #         str(content_ollama_result)

        write_content_to_html(title, response_web, ollama_result, today_date, now, page_url)

    else:
        print(f'Failed to retrieve {page_url}. Status code: {response_web.status_code}')

        ollama_result = f'Failed to retrieve {page_url}. Status code: {response_web.status_code}'

    return ollama_result
