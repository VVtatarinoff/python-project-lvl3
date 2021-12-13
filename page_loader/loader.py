import os
import re
import requests
from operator import truth
from fake_useragent import UserAgent
from page_loader.page import Page


def generate_file_name(from_path, put_extension=False):
    url_split = re.split(r"[\W]+", from_path)
    url_split = list(filter(truth, url_split))
    if put_extension:
        extension = url_split.pop()
        url_split[-1] = f"{url_split[-1]}.{extension}"
    file_name = '-'.join(url_split[1:])
    return file_name


def save_to_path(content, mode, path):
    with open(path, mode) as file:
        file.write(content)
    print("записан, ", path)


def upload_from_web(url, path_to_save=None):
    ua = UserAgent()
    headers = {'User-Agent': ua.random}
    response = requests.get(url, headers=headers)
    if response.status_code != requests.codes.ok:
        print("адрес некорректный: ", url)
        return False
    content_type = response.headers['content-type']
    if not path_to_save:
        return response.content
    if content_type.lower().startswith('image'):
        mode = 'wb'
    else:
        mode = "w"
    save_to_path(response.content, mode, path_to_save)
    return True


def download(url, directory):
    current_dir = os.getcwd()
    storage_path = os.path.join(current_dir, directory)
    html_name = generate_file_name(url)
    subdirectory = html_name + "_files"
    html_name = html_name + ".html"
    abs_subdirectory = os.path.join(storage_path, subdirectory)
    if not os.path.exists(abs_subdirectory):
        os.mkdir(abs_subdirectory)
    page = Page(upload_from_web(url), url)
    images = page.image_references
    replacements = dict()
    for image in images:
        file_name = generate_file_name(image, put_extension=True)
        file_path = os.path.join(abs_subdirectory, file_name)
        flag = upload_from_web(image, file_path)
        if flag:
            replacements[image] = os.path.join(subdirectory, file_name)
    page.change_image_references(replacements)
    save_to_path(page.html, 'w', os.path.join(storage_path, html_name))
