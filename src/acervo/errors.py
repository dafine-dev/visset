

class TeleclipsException(Exception):
    ...


class IncompleteClipSavingAttemptException(TeleclipsException):
    ...


class UnsupportedLanguageException(TeleclipsException):
    
    def __init__(self, *args: object, language: str = ...) -> None:
        super().__init__(*args)
        self.language = language