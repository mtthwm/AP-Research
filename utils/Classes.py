class StreamRule:
    def __init__(self, id, value, tag):
        self.id = id
        self.value = value
        self.tag = tag

    def __str__(self):
        return f"{self.tag} ({self.value})"