from page_loader.naming import Name


def test_name(name_matching):
    generated_name = Name(name_matching['url'])
    assert name_matching['nickname'] == generated_name.full_name
