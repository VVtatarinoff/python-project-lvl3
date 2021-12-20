from bs4 import BeautifulSoup
import urllib3
import logging


logger = logging.getLogger(__name__)


class Page(BeautifulSoup):

    """
    Экземпляр класса - объект Beutifulsoup с возможностью выделения
    ссылок на доменные ресурсы и замена их на ссылки,
    переданные в аргументоах
    """
    LINKS_PATTERN = {'img': 'src', 'link': 'href', 'script': 'src'}

    def __init__(self, html, url):
        self.url = url
        self.parsed = urllib3.util.parse_url(self.url)
        super().__init__(html, "html.parser")
        self.domain_links = self._get_links()

    def _get_domain_path(self, path):
        source_parsed = urllib3.util.parse_url(path)
        normolized_source = None
        if source_parsed.scheme:
            if source_parsed.host != self.parsed.host:
                normolized_source = None
            else:
                normolized_source = path
        else:
            source_parsed = source_parsed._replace(scheme=self.parsed.scheme)
            source_parsed = source_parsed._replace(host=self.parsed.host)
            normolized_source = source_parsed.url
        return normolized_source

    def _get_links(self):
        links = dict()
        for tag, atrr in self.LINKS_PATTERN.items():
            for item in self.find_all(tag):
                reference = item.get(atrr)
                if not reference:
                    continue
                normolized_source = self._get_domain_path(reference)
                if not normolized_source:
                    continue
                previous_items = links.setdefault(normolized_source, [])
                previous_items.append(item)
                links[normolized_source] = previous_items
        logger.debug(f'extracted {len(links)} domain names')
        return links

    @property
    def link_references(self):
        return self.domain_links.keys()

    def change_links(self, new_links):
        logger.debug(f'started to rename {len(new_links)} html domain names')
        for old_link, new_link in new_links.items():
            tags = self.domain_links[old_link]
            for tag in tags:
                attr = self.LINKS_PATTERN[tag.name]
                tag[attr] = new_link
                logger.debug(f'{old_link} CHANGED TO {new_link}')

    @property
    def html(self):
        return self.prettify()
