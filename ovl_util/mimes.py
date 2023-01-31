from dataclasses import dataclass


# @dataclass(init=False, repr=True, eq=True, order=False, unsafe_hash=False, frozen=False, )
@dataclass
class Mime:
	name: str
	hash: int
	version: int
	triplets: list
	pool: int
	set_pool: int = 0

	@property
	def class_name(self):
		return self.name.split(":")[1]

	@property
	def ext(self):
		return f".{self.name.split(':')[2]}"

