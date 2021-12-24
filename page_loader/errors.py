class MyError(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class NoPermission(MyError):
    def __init__(self, *args):
        super().__init__(*args)


class NoDirectory(MyError):
    def __init__(self, *args):
        super().__init__(*args)


class NoConnection(MyError):
    def __init__(self, *args):
        super().__init__(*args)


class WrongStatusCode(MyError):
    def __init__(self, *args):
        super().__init__(*args)
