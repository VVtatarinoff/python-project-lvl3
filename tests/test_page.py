from page_loader.page import Page
from bs4 import BeautifulSoup


def test_page(fake_urls):
    page = Page(fake_urls.initial_html, fake_urls.url)
    domain_links = page.link_references
    assert len(domain_links) == 1
    assert fake_urls.url_file in domain_links
    replacement = {fake_urls.url_file: fake_urls.path_to_saved_file}
    page.change_links(replacement)
    required_html = BeautifulSoup(fake_urls.modified_html,
                                  "html.parser").prettify()
    assert page.html == required_html
