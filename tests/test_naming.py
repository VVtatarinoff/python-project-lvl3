from page_loader.naming import ConvertUrlToName


def test_name(name_matching):
    generated_name = ConvertUrlToName(name_matching['url'])
    assert name_matching['nickname'] == generated_name.full_name
