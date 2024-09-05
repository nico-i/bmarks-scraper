import re

class WhitelistPattern:
	"""A single whitelist pattern.    
	
	Follows the standard .gitignore pattern syntax -> https://git-scm.com/docs/gitignore/en#_pattern_format
	"""
	# pattern string
	pattern: str

	def __init__(self, pattern: str) -> None:
		# Validate pattern
		if not self.__is_valid_pattern(pattern):
			raise ValueError(f"Invalid pattern: \"{pattern}\"")
		self.pattern = pattern

	def __is_valid_pattern(self, pattern: str) -> bool:
		PATTERN_REGEX = re.compile(r'''
		                            ^
		                            (?!.*\s$)                     # No trailing whitespace
		                            (?:
		                                (?:
		                                    [^!#/\[\]]            # Any character except !, #, /, [, or ]
		                                    | \[(?:[^\]\\]|\\.)*\]  # Character class
		                                )+
		                                | (?:                     # Or a pattern starting with /
		                                    /
		                                    (?:
		                                        [^!#/\[\]]
		                                        | \[(?:[^\]\\]|\\.)*\]
		                                    )+
		                                )
		                            )
		                            (?:
		                                /                         # Directory separator
		                                (?:
		                                    [^!#/\[\]]
		                                    | \[(?:[^\]\\]|\\.)*\]
		                                )*
		                            )*
		                            /?                            # Optional trailing slash
		                            $
		                            ''', re.VERBOSE)

		return bool(PATTERN_REGEX.match(pattern))

	def __repr__(self) -> str:
		return self.pattern

