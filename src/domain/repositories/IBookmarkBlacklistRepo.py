from abc import ABC, abstractmethod


class IBookmarkBlacklistRepo(ABC):
    """BlacklistRepo interface"""
    
    @abstractmethod
    def is_bookmark_blacklisted(self, id: int) -> bool:
        pass
