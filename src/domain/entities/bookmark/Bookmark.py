from dataclasses import dataclass

from domain.interfaces.JSONable.JSONable import JSONable


@dataclass
class Bookmark(JSONable):
    """
    A browser bookmark.
    """

    # Bookmark name
    name: str
    # Bookmark URL
    url: str

    def to_json(self):
        return f'{{"name": "{self.name}", "url": "{self.url}"}}'
