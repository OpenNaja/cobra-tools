import os
import io

from pyffi_ext.formats.ms2 import Ms2Format

def get_ms2_name(mdl2_file_path):
	"""Get the ms2 name used by this file"""
	# read the mdl2
	with open(mdl2_file_path, "rb") as mdl2_stream:
		mdl2_data = Ms2Format.Data()
		mdl2_data.inspect(mdl2_stream)
		
		# get old ms2 name
		return mdl2_data.mdl2_header.name.decode()
			
def merge_mdl2s(mdl2_file_paths, out_dir, ms2_output_name="models.ms2"):
	"""Concatenate vert & tri buffers of several mdl2s into one shared ms2"""
	
	os.makedirs(out_dir, exist_ok=True)
	
	ms2_header = None
	buffer_1 = None
	
	# write each model's vert & tri block to a temporary buffer
	temp_vert_writer = io.BytesIO()
	temp_tris_writer = io.BytesIO()
	
	# set initial offset for the first modeldata
	vert_offset = 0
	tris_offset = 0
	
	# go over all input mdl2 files
	for mdl2_file_path in mdl2_file_paths:
		# read the mdl2
		with open(mdl2_file_path, "rb") as mdl2_stream:
			mdl2_data = Ms2Format.Data()
			mdl2_data.inspect(mdl2_stream)
			
			# get old ms2 name
			ms2_name = mdl2_data.mdl2_header.name.decode()
			
			# set new ms2 name
			mdl2_data.mdl2_header.name = ms2_output_name.encode()
			
			# get ms2 buffers
			dir = os.path.dirname(mdl2_file_path)
			ms2_path = os.path.join(dir, ms2_name)
			with open(ms2_path, "rb") as ms2_stream:
				ms2_header = Ms2Format.Ms2InfoHeader()
				ms2_header.read(ms2_stream, data=mdl2_data)
				
				buffer_1_next = ms2_stream.read(ms2_header.bone_info_size)
				# if it already exists, make sure that it's the same
				if buffer_1 and buffer_1 != buffer_1_next:
					raise AttributeError("Can't merge models with different skeletons")
				buffer_1 = buffer_1_next
				
				eoh = ms2_stream.tell()
				for model in mdl2_data.mdl2_header.models:
					# first, get the buffers for this model from the input
					ms2_stream.seek(eoh + model.vertex_offset)
					verts = ms2_stream.read(model.size_of_vertex * model.vertex_count)
					
					ms2_stream.seek(eoh + ms2_header.buffer_info.vertexdatasize + model.tri_offset)
					tris = ms2_stream.read(2 * model.tri_index_count)
					
					# then, write buffer to each output
					temp_vert_writer.write(verts)
					temp_tris_writer.write(tris)
					
					# update mdl2 offset values
					model.vertex_offset = vert_offset
					model.tri_offset = tris_offset
					
					# get offsets for the next model
					vert_offset = temp_vert_writer.tell()
					tris_offset = temp_tris_writer.tell()
		
		# write modified mdl2
		out_mdl2_file_path = os.path.join(out_dir, os.path.basename(mdl2_file_path) )
		with open(out_mdl2_file_path, "wb") as out_mdl2_stream:
			mdl2_data.mdl2_header.write(out_mdl2_stream, data=mdl2_data)
			
	if ms2_header:
			
		# get bytes from IO object
		vert_bytes = temp_vert_writer.getvalue()
		tris_bytes = temp_tris_writer.getvalue()
		
		# modify buffer size
		ms2_header.buffer_info.vertexdatasize = len(vert_bytes)
		ms2_header.buffer_info.facesdatasize = len(tris_bytes)
		
		# create output ms2
		ms2_path = os.path.join(out_dir, ms2_output_name)
		with open(ms2_path, "wb") as out_ms2_stream:
			ms2_header.write(out_ms2_stream, data=mdl2_data)
			out_ms2_stream.write(buffer_1)
			out_ms2_stream.write(vert_bytes)
			out_ms2_stream.write(tris_bytes)


if __name__=='__main__':
	# mismatched buffer 1 (differrent skeleton) throws an error
	# mdl2_file_paths = ("C:/Users/arnfi/Desktop/ovl/Goliath_Frog/goliath_frog.mdl2", "C:/Users/arnfi/Desktop/ovl/Parrot/export/parrot.mdl2")
	# only models that use the same skeleton can be merged
	mdl2_file_paths = ("C:/Users/arnfi/Desktop/ovl/Parrot/parrot.mdl2", "C:/Users/arnfi/Desktop/ovl/Parrot/export/parrot_notail.mdl2")
	
	out_dir = os.path.join(os.getcwd(), "merged")
	# do the actual merging
	merge_mdl2s(mdl2_file_paths, out_dir, ms2_output_name="models.ms2")