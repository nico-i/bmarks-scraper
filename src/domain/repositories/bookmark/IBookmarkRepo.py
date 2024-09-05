from abc import abstractmethod, ABC
from domain.entities.folder import Folder


class IBookmarkRepo(ABC):
	"""BookmarkRepo interface"""

	@abstractmethod
	def get_root_folder(self) -> Folder:
		"""Get the full bookmarks toolbar starting with the root folder.
		
		Returns:
		    _type_: Folder: Full bookmarks toolbar
		"""
		pass 

	@abstractmethod
	def get_whitelisted_root_folder(self) -> Folder:
		"""Get all whitelisted bookmarks of the bookmarks toolbar starting with the root folder.
		
		Returns:
		    _type_: Folder: Full bookmarks toolbar
		"""
		pass
