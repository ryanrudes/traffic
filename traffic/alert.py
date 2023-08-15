class Alert:
    def __init__(
        self,
        id: str,
        message: str,
        notes: str,
        areas: [str],
    ):
        self.id = id
        self.message = message
        self.notes = notes
        self.areas = areas