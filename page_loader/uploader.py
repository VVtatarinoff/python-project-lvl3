import requests
import logging


from fake_useragent import UserAgent
from page_loader.errors import NoConnection

logger = logging.getLogger(__name__)


class Uploader(object):
    def __init__(self, url):
        self.url = url
        self.mime = None
        self.is_text = False
        self.data = self.load_from_web()
        self.saved = False

    def load_from_web(self):
        ua = UserAgent()
        headers = {'User-Agent': ua.random, 'Accept-Encoding': None}
        logger.debug(f'request sent to web, URL: {self.url}')

        try:
            response = requests.get(self.url, headers=headers)
        except requests.exceptions.ConnectionError:
            logger.critical(f'{self.url} raises connection error')
            raise NoConnection
        else:
            status_code = response.status_code
        if status_code != requests.codes.ok:
            logger.critical(f'file "{self.url}" could not be '
                            'recieved from web. Status '
                            f'code {status_code}')
            return None
        content_types = response.headers['content-type'].split(';')
        self.mime = content_types[0].lower()
        self.is_text = True if self.mime.startswith('text') else False
        logger.debug(f'response recieved from web for address {self.url},'
                     f' response status {status_code}, '
                     f'content type {self.mime}')
        logger.debug(f'self.mime_text = {self.is_text}')
        if self.is_text:
            return response.text
        return response.content

    def save(self, path):
        if not self.data:
            logger.critical(f'file "{path}"'
                            ' has no data to save')
            return
        mode = 'w' if self.is_text else 'wb'
        with open(path, mode) as file:
            try:
                file.write(self.data)
            except Exception:
                logger.critical(f'file "{path}", mode {mode}'
                                ' unable to save to disk')
                raise Exception
            else:
                logger.debug(f'file '
                             f' saved to {path}')
                self.saved = True

    @property
    def content(self):
        return self.data

    @content.setter
    def content(self, data):
        self.data = data
