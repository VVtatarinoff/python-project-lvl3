import os
import requests
from fake_useragent import UserAgent
from page_loader.naming import Name
import logging

logger = logging.getLogger(__name__)


class Uploader(object):
    def __init__(self, url):
        self.url = url
        self.file_name = Name(url)
        self.mode = 'w'
        self.data = self.load_from_web()

    def load_from_web(self):
        ua = UserAgent()
        headers = {'User-Agent': ua.random}
        logger.debug(f'request sent to web, adress {self.url}')
        response = requests.get(self.url, headers=headers)
        logger.debug(f'response recieved from web for adress {self.url},'
                     ' response staus {response.status_code}')
        if response.status_code != requests.codes.ok:
            logger.warning(f'file "{self.url}" could not be '
                           'recieved from web. status '
                           'code {response.status_code}')
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
            logger.warning(f'file "{self.file_name.full_name}"'
                           ' has no data to save')
            return False
        destination = os.path.join(path, self.file_name.full_name)
        with open(destination, self.mode) as file:
            try:
                file.write(self.data)
            except Exception:
                logger.warning(f'file "{self.file_name.full_name}"'
                               ' unable to save to disk')
                return False
            else:
                logger.debug(f'file "{self.file_name.full_name}"'
                             ' saved to {destination}')
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
