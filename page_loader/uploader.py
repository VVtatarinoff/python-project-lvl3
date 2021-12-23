import os.path
import requests
import logging

from fake_useragent import UserAgent

from page_loader.errors import MyError
from page_loader.naming import ConvertUrlToName

logger = logging.getLogger(__name__)


class Uploader(object):
    """
    Объект класса проверяет переданную ссылку, формирует (при
    необходимости имя файла) и скачивает в указанную директорию или
    просто передает содержимое как в переменную
    Принимает на вход url, опционально- путь до директории, имя файла
    В начале проиcходит подготовка stream, проверка на валидность.
    Если не задано имя файла - получение имени на основе
    url и MIME, используя класс  ConvertUrlToName
    """

    def __init__(self, url, directory=None,
                 file_name=None):
        self.CHUNK_SIZE = 1024
        self.url = url
        if directory:
            self.directory = directory
        else:
            self.directory = os.getcwd()
        self._file_name = file_name
        self._mime = ''
        self.error = ""
        self.saved = False

    def _send_request(self, stream=True):
        ua = UserAgent()
        headers = {'User-Agent': ua.random, 'Accept-Encoding': None}
        logger.debug(f'request sent to web, URL: {self.url}')
        try:
            response = requests.get(self.url, headers=headers, stream=stream)
        except requests.exceptions.ConnectionError:
            logger.warning(f'{self.url} raises connection error')
            self.error = f'could not establish the connection to {self.url}'
            return
        if not response.ok:
            logger.warning(f'file "{self.url}" could not be '
                           'received from web. Status of response: '
                           f'code {response.status_code}')
            self.error = (f'the response from {self.url} received with '
                          f'status code "{response.status_code}"')
            return
        return response

    def _check_response(self, response):
        if 'content-type' in response.headers:
            content_types = response.headers['content-type'].split(';')
            self._mime = content_types[0].lower()
        if not self._file_name:
            self._file_name = ConvertUrlToName(self.url, self._mime).full_name
        logger.debug(f'response received from web for address {self.url},'
                     f' response status {response.status_code}, '
                     f'content type {self._mime}')

    def save_from_web(self):
        response = self._send_request()
        if not response:
            return
        self._check_response(response)
        with open(os.path.join(self.directory, self._file_name), 'wb') as file:
            try:
                for chunk in response.iter_content(chunk_size=self.CHUNK_SIZE):
                    file.write(chunk)
            except Exception as e:
                logger.warning(f'file "{self._file_name}"'
                               ' unable to save to disk')
                self.error = (f'during saving "{self._file_name}" raised '
                              f'"{e}"')
            else:
                logger.debug(f'file {self._file_name}'
                             f' saved to {self.directory}')
                self.saved = True

    def load_content(self):
        response = self._send_request()
        if response:
            self._check_response(response)
            return response.text
        raise MyError(self.error)

    @property
    def file_name(self):
        return self._file_name
