import os
from domain.value_objects.whitelist.Whitelist import Whitelist
from domain.repositories.whitelist.IWhitelistRepo import IWhitelistRepo


class FSWhitelistRepo(IWhitelistRepo):
    """Whitelist repository implementation based on a whitelist file in the filesystem."""
    
    __whitelist: Whitelist

    def __init__(self, whitelist_path: str):
        if not os.path.exists(whitelist_path):
            raise FileNotFoundError(f"Whitelist file not found: {whitelist_path}")
        
        with open(whitelist_path, "r", encoding="utf-8") as f:
            whitelist_file_content = f.read()
            self.__whitelist = Whitelist(whitelist_file_content=whitelist_file_content)
 
    def get_whitelist(self) -> list[str]:
        return self.__whitelist