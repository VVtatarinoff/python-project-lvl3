from page_loader.naming import ConvertUrlToName


def test_name(name_matching):
    generated_name = ConvertUrlToName(name_matching['url'])
    assert name_matching['nickname'] == generated_name.full_name


def test_override_suffix():
    generated_name = ConvertUrlToName('https://home.com/logger.css',
                                      'text/html')
    assert generated_name.full_name == 'home-com-logger-css.html'
