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

        root_folder_json = self.__bkmks_repo.get_root_folder(whitelist=self.__whitelist)

        json_dict = {}
        json_dict["created"] = datetime.now().isoformat()
        json_dict["bookmarks"] = json.loads(root_folder_json.to_json())

        json_str = json.dumps(json_dict, indent=4, ensure_ascii=False)

        return json_str
