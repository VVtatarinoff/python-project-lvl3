import logging
import mimetypes
from operator import truth
import pathlib
import re

from urllib3.util import parse_url

logger = logging.getLogger(__name__)


def extract_suffix(path):
    if not path or path.endswith('/'):
        return '.html'
    suffix = pathlib.PurePath(path).suffix
    if not suffix:
        return '.html'
    return suffix


def create_short_name(source_name):
    chunks = re.split(r"[_\W]+", source_name)
    chunks = list(filter(truth, chunks))
    return '-'.join(chunks)


def create_name_from_url(url, mime=''):
    parse = parse_url(url)
    path = parse.path if parse.path else ""
    predifined_suffix = mimetypes.guess_extension(mime)
    suffix = predifined_suffix if predifined_suffix else extract_suffix(path)
    if path.endswith(suffix):
        path = path[:-len(suffix)]
    netloc = parse_url(url).netloc
    logger.debug(f'for {url} extracted "{suffix}" extension')
    short_name = create_short_name(netloc + path)
    logger.debug(f'for {url} created "{short_name}" short_name')
    return short_name + suffix
