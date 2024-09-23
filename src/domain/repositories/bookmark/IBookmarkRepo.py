from abc import abstractmethod, ABC
from domain.entities.folder import Folder
from domain.entities.whitelist.Whitelist import Whitelist


class IBookmarkRepo(ABC):
    """BookmarkRepo interface"""

    @abstractmethod
    def get_bkmks(self, whitelist: Whitelist = None) -> Folder:
        """Get all bookmarks toolbar starting from the root. Only returns whitelisted bookmarks if a whitelist is passed.

        Returns:
            _type_: List[Union[Folder, Bookmark]]: All bookmarks
        """
        pass
