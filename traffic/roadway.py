class Roadway:
    def __init__(
        self,
        name: str,
        sort_order: str,
    ):
        self.name = name
        self.sort_order = int(sort_order)