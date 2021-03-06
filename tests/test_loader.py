import pytest
import os
from page_loader.loader import download
from bs4 import BeautifulSoup


def test_loader(fake_urls, temp_directory, requests_mock):
    # ссылка на исходную страницу
    requests_mock.get(fake_urls.url,
                      **fake_urls.mock_page_data)
    requests_mock.get(fake_urls.url_file,
                      **fake_urls.mock_domain_data)
    # fake_urls.mock_adresses(requests_mock.get)()
    file_name = fake_urls.path_to_saved_page
    expected_path = os.path.join(temp_directory.name, file_name)
    created_path = download(fake_urls.url, temp_directory.name)
    assert expected_path == created_path
    # проверка основного файла
    with open(expected_path) as file:
        text = file.read()
    created_html = BeautifulSoup(text, "html.parser").prettify()
    required_html = BeautifulSoup(fake_urls.modified_html,
                                  "html.parser").prettify()
    assert created_html == required_html
    # проверка файла в *_files директории
    file_name = fake_urls.path_to_saved_file
    with open(os.path.join(temp_directory.name, file_name),
              fake_urls.read_mode) as file:
        assert fake_urls.file_content == file.read()


# тестируем неудачную загрузку доменного файла - исключения быть не должно
# возвращается статус ответа 404, но программа должна работать дальше
# все, кроме доменного файла должно присутствовать
@pytest.mark.parametrize('code', [404, 500])
def test_loader_wrong(fake_urls, temp_directory, requests_mock, code):
    requests_mock.get(fake_urls.url,
                      **fake_urls.mock_page_data)
    url_dictionary = fake_urls.mock_domain_data
    url_dictionary['status_code'] = code
    requests_mock.get(fake_urls.url_file, **url_dictionary)

    download(fake_urls.url, temp_directory.name)
    files_directory = fake_urls.path_to_saved_file
    directory = os.path.join(temp_directory.name,
                             os.path.dirname(files_directory))
    assert os.path.exists(directory)
    assert len(os.listdir(directory)) == 0
    file = os.path.join(directory, files_directory)
    assert not os.path.exists(os.path.join(directory, file))
