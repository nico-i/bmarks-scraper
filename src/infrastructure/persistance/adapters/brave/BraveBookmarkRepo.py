import json
import os
import platform
from typing import List, Union
from domain.entities.bookmark.Bookmark import Bookmark
from domain.entities.folder.Folder import Folder
from domain.repositories.IBookmarkRepo import IBookmarkRepo


class BraveBookmarkRepo(IBookmarkRepo):
    """Bookmark repository implementation for Brave."""
    
    __brave_bookmarks: List[Union[Folder, Bookmark]]
    
    def __init__(self, brave_bookmarks_path: str = None):
        """Initialize the BraveBookmarkRepo.
        
        Args:
            brave_bookmarks_path (_type_: str or None): Path to the Brave bookmarks file
        """
        brave_bookmarks_path = brave_bookmarks_path or self.__get_brave_bookmarks_export_path()
        
        bookmarks_export = None
        with open(brave_bookmarks_path, "r", encoding="utf-8") as f:
            bookmarks_export = json.load(f)
            
        self.__brave_bookmarks = self.__parse_bookmarks(bookmarks_export)
    
    def get_root_folder(self):
        return self.__brave_bookmarks

    def __get_brave_bookmarks_export_path(self):
        """Retrieve the path to the Brave bookmarks file.

        Raises:
            OSError: Unsupported operating system
            FileNotFoundError: Brave bookmarks file not found

        Returns:
            _type_: str: Path to the Brave bookmarks file
        """
        maybe_brave_bookmarks_path = os.getenv("BRAVE_BOOKMARKS_PATH")
        
        if not maybe_brave_bookmarks_path:
            system = platform.system()
            if system == "Windows":
                maybe_brave_bookmarks_path = os.path.expandvars(r"%LOCALAPPDATA%\BraveSoftware\Brave-Browser\User Data\Default\Bookmarks")
            elif system == "Darwin":  # macOS
                maybe_brave_bookmarks_path = os.path.expanduser("~/Library/Application Support/BraveSoftware/Brave-Browser/Default/Bookmarks")
            elif system == "Linux":
                maybe_brave_bookmarks_path = os.path.expanduser("~/.config/BraveSoftware/Brave-Browser/Default/Bookmarks")
            else:
                raise OSError(f"Unsupported operating system: {system}")
        
        if not os.path.exists(maybe_brave_bookmarks_path):
            raise FileNotFoundError(f"Brave bookmarks file not found: {maybe_brave_bookmarks_path}, try setting the BRAVE_BOOKMARKS_PATH environment variable if the file is in a custom location.")
        
        return maybe_brave_bookmarks_path
    
    def __rec_parse__brave_bookmark(self, bookmark_or_folder: dict) -> Union[Folder, Bookmark]:
        """Recursively parse a Brave bookmark or folder.
        
        Args:
            bookmark_or_folder (_type_: dict): Brave bookmark or folder
            
        Returns:
            _type_: Union[Folder.Folder, Bookmark.Bookmark]: Folder or Bookmark instance
        """
        if "type" not in bookmark_or_folder:
            raise ValueError("Invalid Brave bookmark or folder: missing 'type' key")
        
        if bookmark_or_folder["type"] == "folder":
            if "children" not in bookmark_or_folder:
                raise ValueError("Invalid Brave folder: missing 'children' key")
            
            children = [self.__rec_parse__brave_bookmark(child) for child in bookmark_or_folder["children"]]
            return Folder(name=bookmark_or_folder["name"], children=children)
        elif bookmark_or_folder["type"] == "url":
            if "url" not in bookmark_or_folder:
                raise ValueError("Invalid Brave bookmark: missing 'url' key")
            
            return Bookmark(name=bookmark_or_folder["name"], url=bookmark_or_folder["url"])
        else:
            raise ValueError(f"Invalid Brave bookmark or folder: unsupported type '{bookmark_or_folder['type']}'")
    
    def __parse_bookmarks(self, bookmarks_export: dict) -> Folder:
        """Parse the Brave bookmarks export into a list of Folder and Bookmark instances.
        
        Args:
            bookmarks_export (_type_: dict): Brave bookmarks export
            
        Returns:
            _type_: Folder: Bookmarks root folder
        """
        if "roots" not in bookmarks_export:
            raise ValueError("Invalid Brave bookmarks export: missing 'roots' key")
        
        if "bookmark_bar" not in bookmarks_export["roots"]:
            raise ValueError("Invalid Brave bookmarks export: missing 'bookmark_bar' key")
        
        bookmarks_bar_folder: Folder = self.__rec_parse__brave_bookmark(bookmarks_export["roots"]["bookmark_bar"])
        
        bookmarks_bar_folder.name = "root"
        
        return bookmarks_bar_folder
        
        
        