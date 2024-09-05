from abc import abstractmethod, ABC
from domain.entities.folder import Folder
from domain.repositories.bookmark.IBookmarkRepo import IBookmarkRepo


class IWhitelistedBookmarkRepo(IBookmarkRepo, ABC):
	"""Whitelisted bookmark repository interface"""

	@abstractmethod
	def get_whitelisted_root_folder(self) -> Folder:
		"""Get all whitelisted bookmarks of the bookmarks toolbar starting with the root folder.
		
		Returns:
		    _type_: Folder: Full bookmarks toolbar
		"""
		pass
