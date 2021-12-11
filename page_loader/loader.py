import os
import re
from bs4 import BeautifulSoup
import requests
from operator import truth
import urllib3
from fake_useragent import UserAgent
from page_loader.page import Page


CURRENT_DIR = os.getcwd()


def generate_file_name(from_path):
    url_split = re.split(r"[\W]+", from_path)
    url_split = list(filter(truth, url_split))
    extension = url_split.pop()
    url_split[-1] = f"{url_split[-1]}.{extension}"
    file_name = '-'.join(url_split[1:])
    return file_name

#
#def download(url, directory):
#    ua = UserAgent()
#    storage_path = os.path.join(CURRENT_DIR, directory)
#    file_name = generate_file_name(url)
#    headers = {'User-Agent': ua.random}
    # parsed = urllib3.util.parse_url(url)
#    response = requests.get(url, headers=headers)
#    with open(os.path.join(storage_path, file_name), 'w') as file:
#        file.write(response.text)
def extract_images(page):
    soup = BeautifulSoup(page.get_html(), "html.parser")
    images = dict()
    for image in  soup.find_all('img'):
        source = image['src']
        source_parsed = urllib3.util.parse_url(source)
        page_source = page.get_parsed()
        normolized_source = source
        if source_parsed.scheme:
            if source_parsed.host != page_source.host:
                normolized_source = None
        else:
            source_parsed = source_parsed._replace (scheme = page_source.scheme)
            source_parsed = source_parsed._replace (host = page_source.host)
            normolized_source = source_parsed.url
        if normolized_source:
            images[source] = normolized_source
    return images

def load_images(images_ref, path, dir):
    dir_name = os.path.join(path, dir)
    try:
        os.mkdir(dir_name)
    except:
        pass
    new_images = dict()
    for ref_short, ref_full in images_ref.items():
        ua = UserAgent()
        headers = {'User-Agent': ua.random}
        response = requests.get(ref_full, headers=headers)
        if response.status_code != requests.codes.ok:
            print("адрес с картинкой некорректнй: ", ref_full)
            continue
        content_type = response.headers['content-type']
        if not content_type.lower().startswith('image'):
            print("по адресу нет картинки ", ref_full)
            continue
        file_name = generate_file_name(ref_full)

        with open(os.path.join(dir_name, file_name), 'wb') as file:
            file.write(response.content)
            print("Записан ", file_name)
        
        new_images[ref_short] = os.path.join(dir, file_name)
    return new_images

def change_image_link(page, new_links):
    soup = BeautifulSoup(page.get_html(), "html.parser")
    for image in  soup.find_all('img'):
        print(image)
        image['src'] = new_links[image['src']]
        print(image)
    page.html = soup.prettify()

def download(url, directory):
    storage_path = os.path.join(CURRENT_DIR, directory)
    page = Page(url, storage_path)
    file_name = page.get_file_name()
    files_directory = f"{file_name}_files"
    images = extract_images(page)
    new_links = load_images(images, storage_path, files_directory)
    change_image_link(page, new_links)
    with open(os.path.join(storage_path, file_name), 'w') as file:
        file.write(page.get_html())