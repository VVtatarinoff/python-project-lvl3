import os
import logging
from progress.bar import Bar
from page_loader.page import Page
from page_loader.uploader import Uploader
from page_loader.errors import NoDirectory, NoContent
from page_loader.errors import FileSaveError


logger = logging.getLogger(__name__)


def download(url, directory):  # noqa C901
    if not url:
        logger.critical('url to upload is empty')
        return
    current_dir = os.getcwd()
    storage_path = os.path.join(current_dir, directory)

    if not os.path.exists(storage_path):
        logger.critical(f"directory '{storage_path}' doesn't exist")
        raise NoDirectory(f"{storage_path} doesn't exist")

    # загружаем и парсим главную страницу
    logger.debug('loading main html')
    html_main = Uploader(url)
    logger.debug(f'recieved content type for main page'
                 f'{type(html_main.content)}')
    if not html_main.content:
        logger.critical(f'unable to html from {url}')
        raise NoContent
    page_structure = Page(html_main.content, url)
    logger.debug('recieved structure of main html')

    # вычисляем ссылки на директории
    subdirectory = html_main.body_name + '_files'
    abs_subdirectory = os.path.join(storage_path, subdirectory)
    path_to_html = os.path.join(storage_path, html_main.name)

    # создаем поддиректорию для доменных файлов
    if not os.path.exists(abs_subdirectory):
        os.mkdir(abs_subdirectory)
        logger.debug(f"directory {abs_subdirectory} created")
    else:
        logger.info(f"directory {abs_subdirectory} exists, no need to rewrite")

    # получаем доменные ссылки и выгружаем файлы
    domain_links = page_structure.link_references
    replacements = dict()
    bar = Bar(message='Saving files ', max=len(domain_links) + 1)
    for link in domain_links:
        web_data = Uploader(link)
        web_data.save(abs_subdirectory)
        bar.next()
        print(' ', link)
        if web_data:
            replacements[link] = os.path.join(subdirectory, web_data.name)

    # подменяем ссылки в html, записываем обновленный файл
    page_structure.change_links(replacements)
    logger.debug('generating updated HTML')
    html_main.content = page_structure.html
    logger.debug('saving updated HTML')
    html_main.save(storage_path)
    bar.next()
    print(' ', html_main.name)
    bar.finish()
    if html_main:
        return path_to_html
    else:
        logger.critical('unable to save updated HTML to file')
        raise FileSaveError
