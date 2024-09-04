from abc import ABC, abstractmethod

class JSONable(ABC):
	@abstractmethod
	def to_json(self) -> str:
		pass

	@staticmethod
	@abstractmethod
	def from_json(json: str) -> 'JSONable':
		pass
