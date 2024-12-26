from yaml.loader import SafeLoader
import yaml
import requests
import pandas as pd
import re
import time

def get_headers():

    with open("brave_cred.yaml") as f:
        conf = yaml.load(f, Loader=SafeLoader)

    apitoken = conf['brave_search']['apikey']

    url = "https://api.search.brave.com/res/v1/news/search"
    #rl = "https://api.search.brave.com/res/v1/web/search?q=APT41"
    headers = {
        "Accept": "application/json",
        "Accept-Encoding": "gzip",
        "X-Subscription-Token": apitoken,

    }

    return headers, url


def brave_search(q, count, offset, freshness):

    headers, url = get_headers()

    type_list = []
    title_list = []
    url_list = []
    description_list = []
    age_list = []
    page_age_list = []

    for off in range(0, offset):

        query = {
            "q": q,
            "count": count
            #"offset": off
            #"freshness": freshness
        }

        response = requests.get(url, params=query, headers=headers)

        print(response.status_code)

        time.sleep(3)

        try:
            for result in response.json()["results"]:

                """Check if description of search result contains search term to
                ensure relevance of search result"""

                match = re.search("Veeva Systems", result["description"])

                if match:

                    print(result["title"])

                    type_list.append(result["type"])
                    title_list.append(result["title"])
                    url_list.append(result["url"])
                    description_list.append(result["description"])
                    age_list.append(result["age"])
                    page_age_list.append(result["page_age"])

                else:

                    continue

        except KeyError:

            continue

    data = {

        "type": type_list,
        "title": title_list,
        'url': url_list,
        'desc': description_list,
        'age': age_list,
        'page age': page_age_list

    }

    df = pd.DataFrame(data)

    return df
