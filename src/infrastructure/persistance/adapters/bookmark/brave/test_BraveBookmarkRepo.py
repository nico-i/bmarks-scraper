import os
import pytest

from domain.entities.bookmark.Bookmark import Bookmark
from domain.entities.folder.Folder import Folder
from infrastructure.persistance.adapters.bookmark.brave.BraveWhitelistedBookmarkRepo import BraveWhitelistedBookmarkRepo
from infrastructure.persistance.adapters.whitelist.fs.FSWhitelistRepo import FSWhitelistRepo

mock_brave_export_path = f"{os.path.dirname(__file__)}/__mocks__/mock_brave_export.json"

mock_whitelist_path = f"{os.path.dirname(__file__)}/__mocks__/.bkmks_wl"

class TestBraveBookmarkRepo:
	def test_get_full_toolbar(self):
		brave_bookmark_repo = BraveWhitelistedBookmarkRepo(brave_bookmarks_path=mock_brave_export_path)
		full_toolbar = brave_bookmark_repo.get_root_folder()
  
		expected_bookmarks_folder = Folder(name="root", children=[
			Folder(name="Dev", children=[
				Folder(name="Inspiration", children=[Bookmark(name="Yasoob Khalid", url="https://yasoob.me/")]),
				Bookmark(name="Backdrop Build", url="https://backdropbuild.com/v3/cv-ops"),
			]),
		])

		assert full_toolbar == expected_bookmarks_folder
  
	def test_get_whitelisted_toolbar(self):
		whitelisted_repo = FSWhitelistRepo(whitelist_path=mock_whitelist_path)
		brave_whitelisted_bookmark_repo = BraveWhitelistedBookmarkRepo(brave_bookmarks_path=mock_brave_export_path, whitelist_repo=whitelisted_repo)
		whitelisted_toolbar = brave_whitelisted_bookmark_repo.get_whitelisted_root_folder()

		raise NotImplementedError("Test not implemented")