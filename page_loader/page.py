from bs4 import BeautifulSoup
import urllib3


class Page(BeautifulSoup):
    def __init__(self, html, url):
        self.html_initial = html
        self.url = url
        self.parsed = urllib3.util.parse_url(self.url)
        super().__init__(html, "html.parser")
        self.images = self._get_images()
        # self.links = self.get_links()

    def _get_domain_path(self, path):
        source_parsed = urllib3.util.parse_url(path)
        normolized_source = None
        if source_parsed.scheme:
            if source_parsed.host != self.parsed.host:
                normolized_source = None
        else:
            source_parsed = source_parsed._replace(scheme=self.parsed.scheme)
            source_parsed = source_parsed._replace(host=self.parsed.host)
            normolized_source = source_parsed.url
        return normolized_source

    def _get_images(self):
        images = dict()
        for image in self.find_all('img'):
            source_initial = image['src']
            normolized_source = self._get_domain_path(source_initial)
            if not normolized_source:
                continue
            previous_images = images.setdefault(normolized_source, [])
            previous_images.append(image)
            images[normolized_source] = previous_images
        return images

    @property
    def image_references(self):
        return set(self.images.keys())

    def change_image_references(self, new_links):
        for old_link, new_link in new_links.items():
            images = self.images[old_link]
            for image in images:
                image['src'] = new_link
        self.images = self._get_images()

    @property
    def html(self):
        return self.prettify()

    def _get_links(self):
        pass
