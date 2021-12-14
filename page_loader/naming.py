import re
from operator import truth
from urllib3.util import parse_url
import logging

logger = logging.getLogger(__name__)


class Name(object):
    def __init__(self, url):
        parse = parse_url(url)
        if parse.path:
            self.path = parse.path
        else:
            self.path = ""
        self.netloc = parse_url(url).netloc
        self._extension = self.extract_extension()
        logger.debug(f'for {url} extracted "{self._extension}" extension')
        self.short_name = self.create_short_name()
        logger.debug(f'for {url} created "{self.short_name}" short_name')

    def extract_extension(self):
        if not self.path or self.path.endswith('/'):
            return '.html'
        n = min(6, len(self.path))
        split = self.path[-n:].split('.')
        if len(split) > 1:
            extension = '.' + split[-1]
            self.path = self.path[:-len(extension)]
            return extension
        return ""

    def create_short_name(self):
        source_name = self.netloc + self.path
        chunks = re.split(r"[_\W]+", source_name)
        chunks = list(filter(truth, chunks))
        return '-'.join(chunks)

    @property
    def full_name(self):
        return self.short_name + self._extension

    @property
    def body_name(self):
        return self.short_name

    @property
    def extension(self):
        return self._extension

    @extension.setter
    def extension(self, new_extension):
        logger.debug(f'for {self.short_name} extension '
                     '"{self._extension}" replaced by "{new_extension}"')
        self._extension = new_extension
