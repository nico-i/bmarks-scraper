import os
import pytest

from domain.repositories import whitelist
from domain.value_objects.whitelist.Whitelist import Whitelist
from infrastructure.persistance.adapters.whitelist.fs.FSWhitelistRepo import FSWhitelistRepo

mock_whitelist_path = f"{os.path.dirname(__file__)}/__mocks__/.bkmks"

class TestWhitelist:
    def test_is_whitelisted(self):
        with open(mock_whitelist_path, "r", encoding="utf-8") as f:
            whitelist_file_content = f.read()

        whitelist = Whitelist(whitelist_file_content=whitelist_file_content)
        assert whitelist.is_whitelisted("Test Bookmark") == True
        assert whitelist.is_whitelisted("Test Bookmark 2") == False
        assert whitelist.is_whitelisted("root folder/") == False
        assert whitelist.is_whitelisted("root folder/Test Bookmark") == True
        assert whitelist.is_whitelisted("test/blacklisted") == False
        assert whitelist.is_whitelisted("test/deep/") == False
        assert whitelist.is_whitelisted("test/deep/folder/") == True
        assert whitelist.is_whitelisted("test/deep/folder/Bookmark") == True
        assert whitelist.is_whitelisted("test/deep/folder/blacklisted bookmark") == False
        assert whitelist.is_whitelisted("test/deep/folder/another bookmark") == True
        assert whitelist.is_whitelisted("test/deep/folder/blacklisted folder/") == False
