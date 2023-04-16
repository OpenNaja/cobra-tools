# START_GLOBALS

import logging

# END_GLOBALS


class DataEntry:

	# START_CLASS

	def update_data(self, datas):
		"""Load datas into this DataEntry's buffers, and update its size values according to an assumed pattern
		data : list of bytes object, each representing the data of one buffer for this data entry"""
		for buffer, data in zip(self.sorted_buffers, datas):
			buffer.update_data(data)
		# update data 0, 1 size
		# total = sum(len(d) for d in datas)
		if len(datas) == 1:
			self.size_1 = len(datas[0])
			self.size_2 = 0
		elif len(datas) == 2:
			self.size_1 = 0
			self.size_2 = sum(len(d) for d in datas)
		elif len(datas) > 2:
			self.size_1 = sum(len(d) for d in datas[:2])
			self.size_2 = sum(len(d) for d in datas[2:])

	@property
	def sorted_buffers(self):
		"""Get buffers sorted by index"""
		return sorted(self.buffers, key=lambda buffer: buffer.index)

	@property
	def buffer_datas(self):
		"""Get data for each buffer"""
		return list(buffer.data for buffer in self.sorted_buffers)

	def __eq__(self, other):
		attr_check = ("buffer_count", "size_1", "size_2")
		same = True
		for attr in attr_check:
			a = getattr(self, attr)
			b = getattr(other, attr)
			if a != b:
				logging.warning(f"Data differs for '{attr}' - {a} vs {b}")
				same = False
		for i, (a, b) in enumerate(zip(self.sorted_buffers, other.sorted_buffers)):
			if a != b:
				logging.warning(f"Buffer {i} differs for {a} vs {b}")
				same = False
		return same
