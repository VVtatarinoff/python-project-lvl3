import re
from operator import truth
from urllib3.util import parse_url
import logging
import pathlib
import mimetypes

logger = logging.getLogger(__name__)


class ConvertUrlToName(object):
    """
    конвертация URL в имя. Для большей точности определения суффикса
    может быть передан MIME из HTTP запроса.
    """
    def __init__(self, url, mime=''):
        parse = parse_url(url)
        if parse.path:
            self.path = parse.path
        else:
            self.path = ""
        if mime:
            predifined_suffix = mimetypes.guess_extension(mime)
        else:
            predifined_suffix = ''
        self.netloc = parse_url(url).netloc
        self._suffix = self.extract_suffix(predifined_suffix)
        logger.debug(f'for {url} extracted "{self._suffix}" extension')
        self.short_name = self.create_short_name()
        logger.debug(f'for {url} created "{self.short_name}" short_name')

    def extract_suffix(self, predefined_suffix):
        if not self.path or self.path.endswith('/'):
            return '.html' if not predefined_suffix else predefined_suffix
        suffix = pathlib.PurePath(self.path).suffix
        if not suffix and not predefined_suffix:
            return ''
        if suffix == predefined_suffix or not predefined_suffix:
            self.path = self.path[:-len(suffix)]
        else:
            suffix = predefined_suffix
        logger.debug(f'for {self.netloc} extracted {suffix} suffix')
        return suffix

    def create_short_name(self):
        source_name = self.netloc + self.path
        chunks = re.split(r"[_\W]+", source_name)
        chunks = list(filter(truth, chunks))
        return '-'.join(chunks)

    @property
    def full_name(self):
        return self.short_name + self._suffix
