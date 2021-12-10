import os
import re
import requests
from operator import truth
# import urllib3
from fake_useragent import UserAgent

CURRENT_DIR = os.getcwd()


def generate_file_name(from_path):
    url_split = re.split(r"[\W]+", from_path)
    url_split = list(filter(truth, url_split))
    file_name = '-'.join(url_split[1:])
    return f"{file_name}.html"


def download(url, directory):
    ua = UserAgent()
    storage_path = os.path.join(CURRENT_DIR, directory)
    print(os.path.exists(storage_path))
    file_name = generate_file_name(url)
    headers = {'User-Agent': ua.random}
    # parsed = urllib3.util.parse_url(url)
    response = requests.get(url, headers=headers)
    with open(os.path.join(storage_path, file_name), 'w') as file:
        file.write(response.text)
