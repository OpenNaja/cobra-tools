class DataEntry:

	# START_CLASS

	def update_data(self, datas):
		"""Load datas into this DataEntry's buffers, and update its size values according to an assumed pattern
		data : list of bytes object, each representing the data of one buffer for this data entry"""
		for buffer, data in zip(self.buffers, datas):
			buffer.update_data(data)
		# update data 0, 1 size
		total = sum(len(d) for d in datas)
		if len(datas) == 1:
			self.size_1 = len(datas[0])
			self.size_2 = 0
		elif len(datas) == 2:
			self.size_1 = 0
			self.size_2 = sum(len(d) for d in datas)
		elif len(datas) > 2:
			self.size_1 = sum(len(d) for d in datas[:-1])
			self.size_2 = len(datas[-1])


	# print(total)
	# print(self.size_1)
	# print(self.size_2)

	def update_buffers(self, ):
		# sort the buffer entries of each data entry by their index
		self.buffers.sort(key=lambda buffer: buffer.index)


	# trim to valid buffers (ignore ones that run out of count, usually zero-sized ones)
	# self.buffers = self.buffers[:self.buffer_count]
	# self.buffers = list(b for b in self.buffers if b.size)

	@property
	def buffer_datas(self):
		"""Get data for each non-empty buffer (should have been sorted before)"""
		return list(buffer.data for buffer in self.buffers if buffer.size)