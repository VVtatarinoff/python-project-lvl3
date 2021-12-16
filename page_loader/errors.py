class MyError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class NoDirectory(MyError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

    def __str__(self):
        return "Directory doesn't exists"


class NoConnection(MyError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class NoContent(MyError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class FileSaveError(MyError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
