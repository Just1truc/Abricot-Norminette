class Section:

    # pylint: disable=R0913, R0902
    def __init__(
        self,
        start: int,
        end: int,
        line_start: int,
        line_end: int,
        column_start: int,
        column_end: int,
        raw: str
    ):
        self.start = start
        self.end = end
        self.line_start = line_start
        self.line_end = line_end
        self.column_start = column_start
        self.column_end = column_end
        self.raw = raw
