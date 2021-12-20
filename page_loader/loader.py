import os
import logging
from progress.bar import Bar
from page_loader.page import Page
from page_loader.uploader import Uploader
from page_loader.errors import MyError


logger = logging.getLogger(__name__)


def load_html_file(path):
    with open(path) as file:
        content = file.read()
    return content


def save_html_file(content, path):
    with open(path, 'w') as file:
        file.write(content)
    return os.path.getsize(path)


def get_html(url, path_to_save):
    if not url:
        logger.critical('url to upload is empty')
        raise MyError
    if not os.path.exists(path_to_save):
        logger.critical(f"directory '{path_to_save}' doesn't exist")
        raise MyError(f"{path_to_save} doesn't exist")
    logger.debug('loading main html')
    html_load = Uploader(url, directory=path_to_save)
    html_load.load_from_web()
    page_file_name = html_load.file_name
    if not html_load.saved:
        raise MyError(f"file {page_file_name} has not been saved")
    if html_load.mime.startswith('html'):
        raise MyError(f"loaded file {page_file_name}, but it's not"
                      f"html-file as MIME is {html_load.mime}")
    logger.debug(f'recieved name of  main html {page_file_name}')
    html_content = load_html_file(os.path.join(path_to_save, page_file_name))
    return html_content, page_file_name


def download(url, directory):  # noqa C901
    current_dir = os.getcwd()
    storage_path = os.path.join(current_dir, directory)

    # загружаем главную страницу
    html_content, page_file_name = get_html(url, directory)
    path_to_html = os.path.join(storage_path, page_file_name)
    page_structure = Page(html_content, url)
    logger.debug('recieved structure of main html')

    # вычисляем ссылки на директории
    subdirectory = page_file_name.replace('.html', '_files')
    abs_subdirectory = os.path.join(storage_path, subdirectory)

    # создаем поддиректорию для доменных файлов
    if not os.path.exists(abs_subdirectory):
        os.mkdir(abs_subdirectory)
        logger.debug(f"directory {abs_subdirectory} created")
    else:
        logger.info(f"directory {abs_subdirectory} exists, no need to rewrite")

    # получаем доменные ссылки и выгружаем файлы
    domain_links = page_structure.link_references
    replacements = dict()
    total_size = 0
    bar = Bar(message='Saving files ', max=len(domain_links) + 1)
    for link in domain_links:
        web_data = Uploader(link, abs_subdirectory)
        web_data.load_from_web()
        if web_data.saved:
            file_name = web_data.file_name
            replacements[link] = os.path.join(subdirectory, file_name)
        bar.next()
        total_size += web_data.size
        print(' ', link, f'size: {web_data.size}')

    # подменяем ссылки в html, записываем обновленный файл
    page_structure.change_links(replacements)
    logger.debug('generating updated HTML')
    html_size = save_html_file(page_structure.html, path_to_html)
    logger.debug('saving updated HTML')
    bar.next()
    print(' ', url, f'size: {html_size}')
    bar.finish()
    total_size += html_size
    print(f'Total bytes saved: {total_size}')
    return path_to_html
