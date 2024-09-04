import json
from attr import dataclass

from domain.interfaces.JSONable.JSONable import JSONable

@dataclass
class Bookmark(JSONable):
	"""
	A browser bookmark.
	"""
	# Bookmark name
	name: str
	# Bookmark URL
	url: str

	def to_json(self):
		return f'{{"type": "{Bookmark.__name__}", "name": "{self.name}", "url": "{self.url}"}}'

	@staticmethod
	def from_json(json_str):
		data = json.loads(json_str)
		return Bookmark(name=data["name"], url=data["url"])