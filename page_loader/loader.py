import os
from page_loader.page import Page
from page_loader.uploader import Uploader


def download(url, directory):
    if not url:
        return
    # загружаем и парсим главную страницу
    html_main = Uploader(url)
    page_structure = Page(html_main.content, url)
    # вычисляем ссылки на директории
    subdirectory = html_main.body_name + '_files'
    current_dir = os.getcwd()
    storage_path = os.path.join(current_dir, directory)
    abs_subdirectory = os.path.join(storage_path, subdirectory)
    path_to_html = os.path.join(storage_path, html_main.name)
    # создаем поддиректорию для доменных файлов
    if not os.path.exists(abs_subdirectory):
        os.mkdir(abs_subdirectory)
    # получаем доменные ссылки и выгружаем файлы
    domain_links = page_structure.link_references
    replacements = dict()
    for link in domain_links:
        web_data = Uploader(link)
        is_success = web_data.save(abs_subdirectory)
        if is_success:
            replacements[link] = os.path.join(subdirectory, web_data.name)
    # подменяем ссылки в html, записываем обновленный файл
    page_structure.change_links(replacements)
    html_main.content = page_structure.html
    is_success = html_main.save(storage_path)
    if is_success:
        return path_to_html
