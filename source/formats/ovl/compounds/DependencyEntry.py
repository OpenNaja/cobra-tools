# START_GLOBALS
import os

# END_GLOBALS


class DependencyEntry:

	# START_CLASS

	@property
	def ext(self):
		return self.ext_raw.replace(":", ".")

	@ext.setter
	def ext(self, e):
		self.ext_raw = e.replace(".", ":")
