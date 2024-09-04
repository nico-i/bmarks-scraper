from os import name
import pytest
from infrastructure.persistance.adapters.brave.BraveBookmarkRepo import BraveBookmarkRepo
from infrastructure.persistance.adapters.brave.test_BraveBookmarkRepo import mock_brave_export_path
from src.domain.entities.bookmark.Bookmark import Bookmark

class TestBookmark:
    
    @pytest.fixture
    def mocked_bookmark(self):
        return Bookmark(name="Yasoob Khalid", url="https://yasoob.me/")
    
    @pytest.fixture
    def mocked_bookmark_json(self):
        return '{"type": "Bookmark", "name": "Yasoob Khalid", "url": "https://yasoob.me/"}'
    
    def test_to_json(self, mocked_bookmark, mocked_bookmark_json):
        json_str = mocked_bookmark.to_json()
        assert json_str == mocked_bookmark_json
        
    def test_from_json(self, mocked_bookmark, mocked_bookmark_json):
        bookmark = Bookmark.from_json(mocked_bookmark_json)
        assert bookmark == mocked_bookmark
        
    