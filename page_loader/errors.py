class MyError(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class NoPermission(MyError):
    def __init__(self, path, *args):
        self.path = path
        super().__init__(*args)

    def __str__(self):
        return f'Access denied for "{self.path}"'


class NoDirectory(MyError):
    def __init__(self, path, *args):
        self.path = path
        super().__init__(*args)

    def __str__(self):
        return f'The directory "{self.path}" does not exist'


class NoConnection(MyError):
    def __init__(self, url, *args):
        self.url = url
        super().__init__(*args)

    def __str__(self):
        return f'could not establish connection' \
               f' to"{self.url}" '


class WrongStatusCode(MyError):
    def __init__(self, code, url, *args):
        self.code = code
        self.url = url
        super().__init__(*args)

    def __str__(self):
        return f'response from URL {self.url} ' \
               f'with error status-code {self.code}'
