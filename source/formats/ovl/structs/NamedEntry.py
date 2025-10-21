# START_GLOBALS
import os

# END_GLOBALS


class NamedEntry:

	# START_CLASS

	@property
	def name(self):
		return self.basename + self.ext

	@name.setter
	def name(self, n):
		self.basename, self.ext = os.path.splitext(n)
