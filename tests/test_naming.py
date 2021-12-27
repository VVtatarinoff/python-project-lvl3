from page_loader.naming import create_name_from_url


def test_name(name_matching):
    generated_name = create_name_from_url(name_matching['url'])
    assert name_matching['nickname'] == generated_name


def test_override_suffix():
    generated_name = create_name_from_url('https://home.com/logger.css',
                                      'text/html')
    assert generated_name == 'home-com-logger-css.html'
