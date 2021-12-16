import requests_mock
import pytest
import os
import sys
from page_loader.loader import download
import tempfile
from bs4 import BeautifulSoup


def test_loader(html_check):
    with tempfile.TemporaryDirectory() as temp_dir:
        with requests_mock.Mocker() as m:
            # ссылка на исходную страницу
            m.get(html_check['url'], headers={'content-type': 'html'},
                  text=html_check['initial_html'])
            # ссылка на файл в домене
            if html_check['text']:
                m.get(html_check['url_file'],
                      headers={'content-type':
                               html_check['content-type']},
                      text=html_check['text'])
            else:
                m.get(html_check['url_file'],
                      headers={'content-type': html_check['content-type']},
                      content=html_check['content'])
            download(html_check['url'], temp_dir)
            # проверка основго файла
            file_name = html_check['name_result_file']
            with open(os.path.join(temp_dir, file_name)) as file:
                text = file.read()
                created_html = BeautifulSoup(text, "html.parser").prettify()
            required_html = BeautifulSoup(html_check['result'],
                                          "html.parser").prettify()
            assert created_html == required_html
            # проверка файла в *_files директории
            file_name = html_check['path_to_file']
            with open(os.path.join(temp_dir, file_name),
                      html_check['read_mode']) as file:
                print(html_check['read_mode'])
                if html_check['read_mode'] == 'r':
                    assert html_check['text'] == file.read()
                else:
                    assert html_check['content'] == file.read()


def test_loader_wrong(wrong_html_domain_subadress):
    with tempfile.TemporaryDirectory() as temp_dir:
        with requests_mock.Mocker() as m:
            m.get(wrong_html_domain_subadress['url'],
                  headers={'content-type': 'html'},
                  text=wrong_html_domain_subadress['html'])
            m.get(wrong_html_domain_subadress['url_file'],
                  status_code=wrong_html_domain_subadress['response_code'])
            download(wrong_html_domain_subadress['url'], temp_dir)
            directory = os.path.join(temp_dir,
                                     wrong_html_domain_subadress['directory'])
            assert os.path.exists(directory)
            assert len(os.listdir(directory)) == 0
            file = os.path.join(directory, wrong_html_domain_subadress['file'])
            assert not os.path.exists(os.path.join(directory, file))


def test_no_directory(html_check):
    with tempfile.TemporaryDirectory() as temp_dir:
        wrong_dir = os.path.join(temp_dir, '/test')
        with pytest.raises(Exception) as excinfo:
            with requests_mock.Mocker() as m:
                # ссылка на исходную страницу
                m.get(html_check['url'], headers={'content-type': 'html'},
                      text=html_check['initial_html'])
                download(html_check['url'], wrong_dir)
        print(sys.exc_info())
        assert 'NoDirectory' in str(excinfo)
