import typing

class Type2:#Sound SFX
	length: int
	sfx_id: int
	consta: int
	constb: int
	didx_id: int
	wem_length: int
	zerosa: int
	zerosb: int
	some_id: int
	constc: int
	constd: int
	conste: int
	floata: float
	zerosc: int
	flag: int
	zerosd: int
	zerose: int
	
	
	def __init__(self,arg=None, template=None):
		self.arg = arg
		self.template= template
	
	def read(self, stream):
		self.length = stream.read_uint()
		self.sfx_id = stream.read_uint()
		self.consta = stream.read_uint()
		self.constb = stream.read_byte()
		self.didx_id = stream.read_uint()
		self.wem_length = stream.read_uint()
		self.zerosa = stream.read_uint()
		self.zerosb = stream.read_uint()
		self.some_id = stream.read_uint()
		self.constc = stream.read_byte()
		self.constd = stream.read_byte()
		if self.constd != 0:
			self.conste = stream.read_byte()
			self.floata = stream.read_float()
		self.zerosc = [stream.read_byte() for _ in range(4)]
		self.flag = stream.read_byte()
		self.zerosd = stream.read_uint()
		self.zerose = stream.read_uint()
	        
	def write(self, stream):
		stream.write_uint(self.length)
		stream.write_uint(self.sfx_id)
		stream.write_uint(self.consta)
		stream.write_byte(self.constb)
		stream.write_uint(self.didx_id)
		stream.write_uint(self.wem_length)
		stream.write_uint(self.zerosa)
		stream.write_uint(self.zerosb)
		stream.write_uint(self.some_id)
		stream.write_byte(self.constc)
		stream.write_byte(self.constd)
		if self.constd != 0:
			stream.write_byte(self.conste)
			stream.write_float(self.floata)
		for item in self.zerosc: stream.write_byte(item)
		stream.write_byte(self.flag)
		stream.write_uint(self.zerosd)
		stream.write_uint(self.zerose)
	
	def __repr__(self):
		s = 'HircPointer'
		s += '\nlength ' + self.length.__repr__()
		s += '\nsfx id ' + self.sfx_id.__repr__()
		s += '\nconsta ' + self.consta.__repr__()
		s += '\nconstb ' + self.constb.__repr__()
		s += '\ndidx id ' + self.didx_id.__repr__()
		s += '\nwem length ' + self.wem_length.__repr__()
		s += '\nzerosa ' + self.zerosa.__repr__()
		s += '\nzerosb ' + self.zerosb.__repr__()
		s += '\nsome id ' + self.some_id.__repr__()
		s += '\nconstc ' + self.constc.__repr__()
		s += '\nconstd ' + self.constd.__repr__()
		if self.constd != 0:
			s += '\nconste ' + self.conste.__repr__()
			s += '\nfloata ' + self.floata.__repr__()
		s += '\nzerosc ' + self.zerosc.__repr__()
		s += '\nflag ' + self.flag.__repr__()
		s += '\nzerosd ' + self.zerosd.__repr__()
		s += '\nzerose ' + self.zerose.__repr__()
		s += '\n'
		return s
