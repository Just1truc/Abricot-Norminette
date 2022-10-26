class TokensError(Exception):
    
    def __init__(self, m='illegal range of tokens requested by the script') -> None:
        super().__init__(m)

class PreprocessingError(Exception):
    
    def __init__(self, m='An error occured while preprocessing code') -> None:
        super().__init__(m)

class UnknownTokenError(Exception):

    def __init__(self, *args: object) -> None:
        super().__init__(*args)