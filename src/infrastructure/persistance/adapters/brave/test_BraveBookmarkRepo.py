import os
import pytest

from domain.entities.bookmark.Bookmark import Bookmark
from domain.entities.folder.Folder import Folder
from infrastructure.persistance.adapters.brave.BraveBookmarkRepo import BraveBookmarkRepo

mock_brave_export_path = f"{os.path.dirname(__file__)}/__mocks__/mock_brave_export.json"

class TestBraveBookmarkRepo:

	@pytest.fixture
	def brave_bookmark_repo(self):
		# Initialize the repository with the test database
		return BraveBookmarkRepo(brave_bookmarks_path=mock_brave_export_path)

	def test_get_full_toolbar(self,brave_bookmark_repo):
		full_toolbar = brave_bookmark_repo.get_root_folder()
  
		expected_bookmarks_folder = Folder(name="root", children=[
			Folder(name="Dev", children=[
				Folder(name="Inspiration", children=[Bookmark(name="Yasoob Khalid", url="https://yasoob.me/")]),
				Bookmark(name="Backdrop Build", url="https://backdropbuild.com/v3/cv-ops"),
			]),
		])

		assert full_toolbar == expected_bookmarks_folder
