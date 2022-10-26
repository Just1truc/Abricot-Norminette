from .section import Section

class Function:

    # pylint: disable=R0913, R0902
    def __init__(
        self,
        prototype: Section,
        body: Section,
        raw: str,
        return_type: str,
        name: str,
        arguments: [str],
    ):
        self.prototype = prototype
        self.body = body
        self.raw = raw
        self.return_type = return_type
        self.name = name
        self.arguments = arguments
