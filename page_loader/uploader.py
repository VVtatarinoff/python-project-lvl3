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
    необходимости имя файла) и скачивает в указанную директорию
    Принимает на вход url, путь до директории, опционально - имя файла,
    максимальный размер файла
    Максимальный размер установлен для дополнительной безопасности кода -
    дабы не переполнить диск
    В начале просиходит подготовка stream, проверка на валидность.
    Если не задано имя файла - получение имени на основе
    url и MIME, используя класс  ConvertUrlToName
    Скачивание и запись идет частями в битовом представлении.
    """

    def __init__(self, url, directory,
                 file_name=None, max_size=1024 * 1024 * 20):
        self.CHUNK_SIZE = 1024
        self.max_size = max_size
        self._size = 0
        self.url = url
        self.directory = directory
        self._file_name = file_name
        self._mime = None
        self.saved = False

    def _send_request(self, stream=True):
        ua = UserAgent()
        headers = {'User-Agent': ua.random, 'Accept-Encoding': None}
        logger.debug(f'request sent to web, URL: {self.url}')
        try:
            response = requests.get(self.url, headers=headers, stream=stream)
        except requests.exceptions.ConnectionError:
            logger.critical(f'{self.url} raises connection error')
            raise MyError(f'could not establish the connection to {self.url}')
        if not response.ok:
            logger.critical(f'file "{self.url}" could not be '
                            'received from web. Status of response: '
                            f'code {response.status_code}')
            raise MyError(f'the response from {self.url} received with '
                          f'status code "{response.status_code}"')
        return response

    def _check_response(self, response):
        content_types = response.headers['content-type'].split(';')
        self._mime = content_types[0].lower()
        if not self._file_name:
            self._file_name = ConvertUrlToName(self.url, self._mime).full_name
        logger.debug(f'response received from web for address {self.url},'
                     f' response status {response.status_code}, '
                     f'content type {self._mime}')
        if 'content-length' in response.headers:
            self._size = int(response.headers["content-length"])
        else:
            logger.critical(f'file "{self.url}"'
                            ' has no data of length')
            logger.debug(f'header : {response.headers}')
            raise MyError(f"{self.url} - error in response's headers:"
                          f"no 'content-length'")
        if self._size > self.max_size:
            logger.critical(f'size of content to download {self._size} exceeds'
                            f' max size {self.max_size}allowed')
            raise MyError(f'size of content to download {self._size} exceeds'
                          f' max size {self.max_size}allowed')
        elif self._size == 0:
            logger.critical(f'file "{self.directory}/{self._file_name}"'
                            ' has no data to save')
            raise MyError(f'size of content to download {self._size} is zero')
        else:
            logger.debug(f'size of content to download is {self._size}')
        return response

    def load_from_web(self):
        response = self._send_request()
        self._check_response(response)
        with open(os.path.join(self.directory, self._file_name), 'wb') as file:
            try:
                for chunk in response.iter_content(chunk_size=self.CHUNK_SIZE):
                    file.write(chunk)
            except Exception as e:
                logger.critical(f'file "{self._file_name}"'
                                ' unable to save to disk')
                raise MyError(f'during saving "{self._file_name}" raised '
                              f'"{e}"')
            else:
                logger.debug(f'file {self._file_name}'
                             f' saved to {self.directory}')
                self.saved = True

    @property
    def file_name(self):
        return self._file_name

    @property
    def mime(self):
        return self._mime

    @property
    def size(self):
        return self._size
