import logging
import os.path
import requests

from fake_useragent import UserAgent

from page_loader.naming import create_name_from_url

CHUNK_SIZE = 1024

logger = logging.getLogger(__name__)


def send_request(url, is_raise=False):
    ua = UserAgent()
    headers = {'User-Agent': ua.random, 'Accept-Encoding': None}
    logger.debug(f'request sent to web, URL: {url}')
    try:
        response = requests.get(url, headers=headers, stream=True)
    except requests.exceptions.ConnectionError:
        logger.warning(f'{url} raises connection error')
        if is_raise:
            message = f'could not establish connection to"{url}" '
            raise requests.exceptions.ConnectionError(message)
        return
    if not response.ok:
        logger.warning(f'file "{url}" could not be '
                       'received from web. Status of response: '
                       f'code {response.status_code}')
        if is_raise:
            message = f'response from URL {url} with error ' \
                      f'status-code {response.status_code}'
            raise requests.exceptions.HTTPError(message)
        return
    logger.debug(f'response received from web for address {url},'
                 f' response status {response.status_code}')
    return response


def get_name(url, response):
    mime = ''
    if 'content-type' in response.headers:
        content_types = response.headers['content-type'].split(';')
        mime = content_types[0].lower()
    file_name = create_name_from_url(url, mime)
    logger.debug(f'generated file name {file_name}')
    return file_name


def save_from_web(url, directory):
    response = send_request(url)
    if not response:
        return
    file_name = get_name(url, response)
    with open(os.path.join(directory, file_name), 'wb') as file:
        try:
            for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                file.write(chunk)
        except PermissionError:
            logger.critical(f"no right so save into '"
                            f"directory '{directory}'")
            raise PermissionError(f'Access denied for "{directory}"')
        else:
            logger.debug(f'file {file_name}'
                         f' saved to {directory}')
            return file_name


def load_content_from_web(url):
    response = send_request(url, is_raise=True)
    logger.debug(f'received response {bool(response)}')
    file_name = get_name(url, response)
    return response.text, file_name
