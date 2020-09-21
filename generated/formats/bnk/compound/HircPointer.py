import typing
from generated.formats.bnk.compound.Type2 import Type2
#from generated.formats.bnk.compound.Type4 import Type4
#from generated.formats.bnk.compound.Type3 import Type3

class HircPointer:

# second Section of a soundback aux
	id: bytes

	# offset into data section
	length: int

	# length of the wem file
	datas: typing.List[int]
	type_2: Type2
	#type_4: Type4
	#type_3: Type3
	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template

	def read(self, stream):
		self.id = stream.read_byte()
		if self.id == 2:
			self.type_2 = stream.read_type(Type2)
		#elif self.id == 4:
		#	self.type_4 = stream.read_type(Type4)
		#elif self.id == 3:
		#	self.type_3 = stream.read_type(Type3)
		else:
			self.length = stream.read_uint()
			self.datas = [stream.read_byte() for _ in range(self.length)]

	def write(self, stream):
		stream.write_byte(self.id)
		if self.id == 2:
			stream.write_type(self.type_2)
		#elif self.id == 4:
		#	stream.write_type(self.type_4)
		#elif self.id == 3:
		#	stream.write_type(self.type_3)
		else:
			stream.write_uint(self.length)
			for item in self.datas: stream.write_byte(item)

	def __repr__(self):
		s = 'HircPointer'
		s += '\nid ' + self.id.__repr__()
		if self.id == 2:
			s += '\ntype 2 ' + self.type_2.__repr__()
		#elif self.id == 4:
		#	s += '\ntype 4 ' + self.type_4.__repr__()
		#elif self.id == 3:
		#	s += '\ntype 3 ' + self.type_3.__repr__()
		else:
			s += '\nlength ' + self.length.__repr__()
			s += '\ndatas ' + self.datas.__repr__()
		s += '\n'
		return s
        

	
#class Type3:#Event Action
	

	        
	        
	        
#class Type5:#Random or Sequence Container

#class Type7:#Actor-Mixer

#class Type14:#Attenuation
