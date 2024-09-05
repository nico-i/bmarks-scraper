
import json
import os
from infrastructure.persistance.adapters.bookmark.brave.BraveBookmarkRepo import BraveBookmarkRepo
from infrastructure.persistance.adapters.whitelist.fs.FSWhitelistRepo import FSWhitelistRepo


def main():
	whitelist_repo = FSWhitelistRepo()
	bookmark_repo = BraveBookmarkRepo()
 
	json_object = json.loads(bookmark_repo.get_root_folder().to_json())
 

	with open("bookmarks.json", "w", encoding="utf-8") as f:    
		f.write(json.dumps(json_object, indent=4, ensure_ascii=False))


if __name__ == "__main__":
	main()
