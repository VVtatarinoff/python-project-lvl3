import logging
import os.path
import requests

from fake_useragent import UserAgent

from page_loader.errors import NoConnection, WrongStatusCode
from page_loader.errors import NoPermission
from page_loader.naming import create_name_from_url


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
        self.error = None
        self.saved = False

    def _send_request(self, stream=True):
        ua = UserAgent()
        headers = {'User-Agent': ua.random, 'Accept-Encoding': None}
        logger.debug(f'request sent to web, URL: {self.url}')
        try:
            response = requests.get(self.url, headers=headers, stream=stream)
        except requests.exceptions.ConnectionError:
            logger.warning(f'{self.url} raises connection error')
            self.error = NoConnection(self.url)
            return
        if not response.ok:
            logger.warning(f'file "{self.url}" could not be '
                           'received from web. Status of response: '
                           f'code {response.status_code}')
            self.error = WrongStatusCode(response.status_code, self.url)
            return
        logger.debug(f'response received from web for address {self.url},'
                     f' response status {response.status_code}')
        return response

    def _get_name(self, response):
        if 'content-type' in response.headers:
            content_types = response.headers['content-type'].split(';')
            self._mime = content_types[0].lower()
        if not self._file_name:
            self._file_name = create_name_from_url(self.url, self._mime)
        logger.debug(f'generated file name {self._file_name}')

    def save_from_web(self):
        response = self._send_request()
        if not response:
            return
        self._get_name(response)
        with open(os.path.join(self.directory, self._file_name), 'wb') as file:
            try:
                for chunk in response.iter_content(chunk_size=self.CHUNK_SIZE):
                    file.write(chunk)
            except PermissionError:
                logger.critical(f"no right so save into '"
                                f"directory '{self.directory}'")
                raise NoPermission(path=self.directory)
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
        logger.debug(f'received response {bool(response)}')
        if response:
            self._get_name(response)
            return response.text
        return None

    @property
    def file_name(self):
        return self._file_name
