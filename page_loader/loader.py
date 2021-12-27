import logging
import os

from progress.bar import Bar

from page_loader.errors import NoPermission, NoDirectory
from page_loader.page import Page
from page_loader.uploader import save_from_web
from page_loader.uploader import load_content_from_web

logger = logging.getLogger(__name__)


def save_html_file(content, path):
    with open(path, 'w') as file:
        file.write(content)


def make_directory(path):
    try:
        os.mkdir(path)
    except PermissionError:
        logger.critical(f"no right so save into directory '{path}'")
        raise NoPermission(path=path)
    except FileNotFoundError:
        logger.critical(f"directory not found '{path}'")
        raise NoDirectory(path)
    except FileExistsError:
        logger.warning(f"directory {path} already exists")
    else:
        logger.debug(f"directory {path} created")


def download(url, directory):  # noqa C901
    logger.debug(f'started download, URL {url}, directory {directory}')
    storage_path = os.path.join(os.getcwd(), directory)
    # загружаем главную страницу
    html_content, page_file_name = load_content_from_web(url)

    # вычисляем ссылки на директории
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
        file_name = save_from_web(link, abs_files_directory)
        if file_name:
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
