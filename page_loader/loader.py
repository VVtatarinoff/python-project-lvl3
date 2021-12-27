import logging
import os

from progress.bar import Bar

from page_loader.errors import MyError, NoPermission, NoDirectory
from page_loader.page import Page
from page_loader.uploader import Uploader


logger = logging.getLogger(__name__)


def save_html_file(content, path):
    with open(path, 'w') as file:
        file.write(content)


def check_data(url, path_to_save):
    if not url:
        logger.critical('url to upload is empty')
        raise MyError('no URL was passed to function')
    if not os.path.exists(path_to_save):
        logger.critical(f"directory '{path_to_save}' doesn't exist")
        raise NoDirectory(path_to_save)


def make_directory(path):
    if os.path.exists(path):
        return
    try:
        os.mkdir(path)
    except PermissionError:
        logger.critical(f"no right so save into directory '{path}'")
        raise NoPermission(path=path)
    logger.debug(f"directory {path} created")


def download(url, directory):  # noqa C901
    logger.debug(f'started download, URL {url}, directory {directory}')
    storage_path = os.path.join(os.getcwd(), directory)
    check_data(url, storage_path)
    # загружаем главную страницу
    html_load = Uploader(url)
    html_content = html_load.load_content()
    if not html_content:
        raise html_load.error
    # вычисляем ссылки на директории
    page_file_name = html_load.file_name
    path_to_html = os.path.join(storage_path, page_file_name)
    files_directory = page_file_name.replace('.html', '_files')
    abs_files_directory = os.path.join(storage_path, files_directory)

    # создаем поддиректорию для доменных файлов
    make_directory(abs_files_directory)

    # получаем доменные ссылки и выгружаем файлы
    page_structure = Page(html_content, url)
    logger.debug('received structure of main html')
    domain_links = page_structure.link_references
    replacements = dict()
    bar = Bar(message='Saving files ', max=len(domain_links) + 1)
    for link in domain_links:
        web_data = Uploader(link, abs_files_directory)
        web_data.save_from_web()
        if web_data.saved:
            file_name = web_data.file_name
            replacements[link] = os.path.join(files_directory, file_name)
        bar.next()

    # подменяем ссылки в html, записываем обновленный файл
    page_structure.change_links(replacements)
    logger.debug('generating updated HTML')
    save_html_file(page_structure.html, path_to_html)
    logger.debug('saving updated HTML')
    bar.next()
    bar.finish()
    return path_to_html
