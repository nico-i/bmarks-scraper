import pytest
from src.domain.entities.bookmark.Bookmark import Bookmark

class TestBookmark:
    
    @pytest.fixture(scope="session")
    def mocked_bookmark(self):
        return Bookmark(name="Test Bookmark", url="https://www.example.com/")
    
    @pytest.fixture(scope="session")
    def mocked_bookmark_json(self):
        return '{"type": "Bookmark", "name": "Test Bookmark", "url": "https://www.example.com/"}'
    
    def test_to_json(self, mocked_bookmark, mocked_bookmark_json):
        json_str = mocked_bookmark.to_json()
        assert json_str == mocked_bookmark_json
        
    