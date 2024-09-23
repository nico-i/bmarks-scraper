from datetime import datetime
import json
from domain.entities.whitelist.Whitelist import Whitelist
from domain.repositories.bookmark.IBookmarkRepo import IBookmarkRepo


class WriterService:
    __bkmks_repo: IBookmarkRepo
    __whitelist: Whitelist

    def __init__(self, bkmks_repo: IBookmarkRepo, whitelist: Whitelist = None):
        self.__bkmks_repo = bkmks_repo
        self.__whitelist = whitelist

    def print_bkmks_json(self):
        """Returns a JSON of all"""

        bkmks_and_folders = self.__bkmks_repo.get_bkmks(whitelist=self.__whitelist)
        bkmks_str = f"[{", ".join([b_or_f.to_json() for b_or_f in bkmks_and_folders])}]"

        json_str = (
            "{"
            + f'"created": "{datetime.now().isoformat()}", "bookmarks": {bkmks_str}'
            + "}"
        )
        return json_str
