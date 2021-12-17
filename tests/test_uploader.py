import requests_mock
import pytest
from page_loader.uploader import Uploader


def test_loader_wrong_adress(fake_urls):
    with pytest.raises(Exception) as excinfo:
        with requests_mock.Mocker() as m:
            fake_urls.mock_adresses(m.get)()
            Uploader(fake_urls.url[:-3])
        assert 'NoConnection' in str(excinfo)


def test_loader_wrong_path(fake_urls):
    with pytest.raises(Exception) as excinfo:
        with requests_mock.Mocker() as m:
            fake_urls.mock_adresses(m.get)()
            test_wrong = Uploader(fake_urls.url)
            test_wrong.save('/asdadaasd')
        assert 'NoDirectory' in str(excinfo)
