import logging
from urllib.parse import urlparse, urljoin

from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class Page(BeautifulSoup):
    """
    Экземпляр класса - объект Beutifulsoup с возможностью выделения
    ссылок на доменные ресурсы и замена их на ссылки,
    переданные в аргументоах
    """
    TAGS_LINK_PATTERN = {'img': 'src', 'link': 'href', 'script': 'src'}

    def __init__(self, html, url):
        self.url = url
        self.parsed = urlparse(self.url)
        super().__init__(html, "html.parser")
        self.tags_with_domain_links = self._get_links()

    def _get_domain_url(self, path):
        url = urlparse(path)
        if url.scheme and url.netloc != self.parsed.netloc:
            return None
        return urljoin(self.url, path)

    def _get_links(self):
        links = dict()
        for tag in self.find_all():
            if tag.name in self.TAGS_LINK_PATTERN:
                attribute = self.TAGS_LINK_PATTERN[tag.name]
                reference = tag.get(attribute)
                if not reference:
                    continue
                domain_url = self._get_domain_url(reference)
                if not domain_url:
                    continue
                previous_items = links.setdefault(domain_url, [])
                previous_items.append(tag)
                links[domain_url] = previous_items
        logger.debug(f'extracted {len(links)} domain names')
        return links

    @property
    def domain_urls(self):
        return self.tags_with_domain_links.keys()

    def change_links(self, new_links):
        logger.debug(f'started to rename {len(new_links)} html domain names')
        for old_link, new_link in new_links.items():
            tags = self.tags_with_domain_links[old_link]
            for tag in tags:
                attr = self.TAGS_LINK_PATTERN[tag.name]
                tag[attr] = new_link
                logger.debug(f'{old_link} CHANGED TO {new_link}')

    @property
    def html(self):
        return self.prettify()
