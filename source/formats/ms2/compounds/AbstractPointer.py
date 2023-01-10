class AbstractPointer:

	# START_CLASS

	def __init__(self, context, arg=None, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.joint = None
		if set_default:
			self.set_defaults()

	def __repr__(self):
		n = self.joint.name if self.joint else None
		return f"{self.index} -> {n}"
