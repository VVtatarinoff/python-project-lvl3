import os
import requests
from fake_useragent import UserAgent
from page_loader.naming import Name


class Uploader(object):
    def __init__(self, url):
        self.url = url
        self.file_name = Name(url)
        self.mode = 'w'
        self.data = self.load_from_web()

    def load_from_web(self):
        ua = UserAgent()
        headers = {'User-Agent': ua.random}
        response = requests.get(self.url, headers=headers)
        if response.status_code != requests.codes.ok:
            return None
        content_type = response.headers['content-type'].lower()
        if content_type.startswith('image'):
            self.mode = 'wb'
            return response.content
        # корректируем расширение файла, т.к. по названию
        # не всегда видно что возвращается страница html
        if content_type.find('html') >= 0:
            self.file_name.extension = '.html'
        self.mode = "w"
        return response.text

    def save(self, path):
        if not self.data:
            return False
        destination = os.path.join(path, self.file_name.full_name)
        with open(destination, self.mode) as file:
            try:
                file.write(self.data)
                print("записан, ", self.file_name.full_name)
            except Exception:
                print("ОШИБКА ЗАПИСИ ", self.file_name.full_name)
                return False
        return True

    @property
    def content(self):
        return self.data

    @content.setter
    def content(self, data):
        self.data = data

    @property
    def name(self):
        return self.file_name.full_name

    @property
    def body_name(self):
        return self.file_name.body_name
