from bs4 import BeautifulSoup
import os
import re
from operator import truth
import urllib3
from fake_useragent import UserAgent
import requests


class Page():
    def __init__(self, adress, path):
        self.url = adress
        self.parsed = urllib3.util.parse_url(self.url)
        self.nikname = self.generate_nick(adress)
        self.path = path
        self.images = None
        self.html = self.get_from_web()


    def generate_nick(self, from_path):
        url_split = re.split(r"[\W]+", from_path)
        url_split = list(filter(truth, url_split))
        file_name = '-'.join(url_split[1:])
        return file_name

    def get_from_web(self):
        ua = UserAgent()
        headers = {'User-Agent': ua.random}
        response = requests.get(self.url, headers=headers)
        return response.text

    def get_html(self):
        return self.html

    def get_file_name(self):
        return self.nikname + '.html'
    
    def get_domain(self):
        return self.parsed['host']

    def get_parsed(self):
        return self.parsed