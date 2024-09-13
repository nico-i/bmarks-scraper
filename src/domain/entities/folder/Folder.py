from typing import List, Union

from attr import dataclass

from domain.entities.bookmark.Bookmark import Bookmark
from domain.interfaces.JSONable.JSONable import JSONable


@dataclass
class Folder(JSONable):
    """
    A folder containing bookmarks and subfolders.
    """

    # Folder name
    name: str
    # Children (sub-folders and bookmarks)
    children: List[Union["Folder", Bookmark]] = []

    def to_json(self) -> str:
        if not all([isinstance(child, JSONable) for child in self.children]):
            raise ValueError("All children must be JSONable")

        return f'{{"type": "{Folder.__name__}", "name": "{self.name}", "children": [{",".join([child.to_json() for child in self.children])}]}}'
