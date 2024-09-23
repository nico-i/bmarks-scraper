from abc import abstractmethod, ABC
from domain.entities.folder import Folder
from domain.entities.whitelist.Whitelist import Whitelist


class IBookmarkRepo(ABC):
    """BookmarkRepo interface"""

    @abstractmethod
    def get_root_folder(self, whitelist: Whitelist = None) -> Folder:
        """Get the full bookmarks toolbar starting with the root folder. Only returns whitelisted bookmarks if a whitelist is passed.

        Returns:
            _type_: Folder: Full bookmarks toolbar
        """
        pass
