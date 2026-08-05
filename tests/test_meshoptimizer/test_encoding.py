"""
Tests for the meshoptimizer Python wrapper.

This file contains tests to verify that the encoding/decoding process
preserves the mesh geometry correctly, handles parameters flexibly,
and properly raises errors when failures occur.
"""
import numpy as np
import pytest
from unittest.mock import patch
from utils.meshoptimizer import (
	encode_vertex_buffer, decode_vertex_buffer,
	encode_index_buffer, decode_index_buffer,
	encode_index_sequence, decode_index_sequence,
	encode_vertex_version, encode_index_version,
	decode_vertex_version, decode_index_version,
	decode_filter_oct, decode_filter_quat, decode_filter_exp
)

@pytest.fixture
def basic_mesh():
	"""Set up test data (a simple cube)."""
	vertices = np.array([
		[-0.5, -0.5, -0.5],
		[0.5, -0.5, -0.5],
		[0.5, 0.5, -0.5],
		[-0.5, 0.5, -0.5],
		[-0.5, -0.5, 0.5],
		[0.5, -0.5, 0.5],
		[0.5, 0.5, 0.5],
		[-0.5, 0.5, 0.5]
	], dtype=np.float32)

	indices = np.array([
		0, 1, 2, 2, 3, 0,
		1, 5, 6, 6, 2, 1,
		5, 4, 7, 7, 6, 5,
		4, 0, 3, 3, 7, 4,
		3, 2, 6, 6, 7, 3,
		4, 5, 1, 1, 0, 4
	], dtype=np.uint32)

	return vertices, indices

def get_triangles_set(vertices, indices):
	"""
	Get a set of triangles from vertices and indices.
	Each triangle is represented as a frozenset of tuples of vertex coordinates.
	This makes the comparison invariant to vertex order within triangles.
	"""
	triangles = set()
	for i in range(0, len(indices), 3):
		v1 = tuple(vertices[indices[i]])
		v2 = tuple(vertices[indices[i+1]])
		v3 = tuple(vertices[indices[i+2]])
		triangle = frozenset([v1, v2, v3])
		triangles.add(triangle)
	return triangles

def test_encode_decode_vertices(basic_mesh):
	"""Test that encoding and decoding vertices preserves the data."""
	vertices, _ = basic_mesh

	encoded_vertices = encode_vertex_buffer(
		vertices,
		len(vertices),
		vertices.itemsize * vertices.shape[1]
	)

	decoded_vertices = decode_vertex_buffer(
		len(vertices),
		vertices.itemsize * vertices.shape[1],
		encoded_vertices
	)

	np.testing.assert_array_almost_equal(vertices, decoded_vertices)

def test_encode_decode_index_buffer(basic_mesh):
	"""Test that encoding and decoding indices preserves the data."""
	vertices, indices = basic_mesh

	encoded_indices = encode_index_buffer(
		indices,
		len(indices),
		len(vertices)
	)

	decoded_indices = decode_index_buffer(
		len(indices),
		4,
		encoded_indices
	)

	original_triangles = get_triangles_set(vertices, indices)
	decoded_triangles = get_triangles_set(vertices, decoded_indices)
	assert original_triangles == decoded_triangles

def test_encode_decode_index_sequence(basic_mesh):
	"""Test that encoding and decoding index sequence preserves the data."""
	vertices, indices = basic_mesh

	encoded_sequence = encode_index_sequence(
		indices,
		len(indices),
		len(vertices)
	)

	decoded_sequence = decode_index_sequence(
		len(indices),
		4,
		encoded_sequence
	)

	original_triangles = get_triangles_set(vertices, indices)
	decoded_triangles = get_triangles_set(vertices, decoded_sequence)
	assert original_triangles == decoded_triangles

def test_encoder_parameter_fallbacks(basic_mesh):
	"""Test that encoders properly derive missing array lengths and sizes."""
	vertices, indices = basic_mesh

	# Passing None for counts/sizes forces the wrapper to calculate them
	encoded_v = encode_vertex_buffer(vertices)
	assert len(encoded_v) > 0

	encoded_i = encode_index_buffer(indices)
	assert len(encoded_i) > 0

	encoded_s = encode_index_sequence(indices)
	assert len(encoded_s) > 0

def test_encode_decode_versions(basic_mesh):
	"""Test the encode and decode version functions and their error handling."""
	vertices, indices = basic_mesh

	# Valid assignments
	encode_vertex_version(1)
	encode_index_version(1)

	# Invalid assignments
	with pytest.raises(ValueError, match="Version must be 0 or 1"):
		encode_vertex_version(2)

	with pytest.raises(ValueError, match="Version must be 0 or 1"):
		encode_index_version(-1)

	# Encode buffers to test version extraction
	enc_v = encode_vertex_buffer(vertices)
	enc_i = encode_index_buffer(indices)

	# Decode versions
	v_ver = decode_vertex_version(enc_v)
	i_ver = decode_index_version(enc_i)

	assert isinstance(v_ver, int)
	assert isinstance(i_ver, int)

def test_decode_vertex_buffer_modes(basic_mesh):
	"""Test raw data typing and 1-component reshaping logic in vertex decoder."""
	vertices, _ = basic_mesh
	enc_v = encode_vertex_buffer(vertices)
	vertex_size = vertices.itemsize * vertices.shape[1]

	# 1. Raw mode (explicit dtype)
	# The wrapper allocates exactly `vertex_count` elements of `dtype`.
	# To prevent buffer overflows, the dtype must accurately reflect the vector size.
	dec_raw = decode_vertex_buffer(
		len(vertices),
		vertex_size,
		enc_v,
		dtype=np.dtype((np.float32, 3))
	)
	assert len(dec_raw) == len(vertices)

	# 2. 1-component reshaping logic (e.g., UV maps or 1D scales)
	flat_verts = np.array([1.0, 2.0, 3.0, 4.0], dtype=np.float32)
	enc_flat = encode_vertex_buffer(flat_verts, vertex_size=4)
	dec_flat = decode_vertex_buffer(len(flat_verts), 4, enc_flat)

	# Array should remain 1D, instead of being reshaped to (N, 1)
	assert dec_flat.shape == (4,)

def test_decode_filters():
	"""Test that filters execute cleanly and return copies of the data."""
	# Octahedral filter expects stride % 4 == 0 (16 bytes is safe for 4 count)
	oct_buffer = np.zeros(16, dtype=np.uint8)
	oct_res = decode_filter_oct(oct_buffer, 4, 4)
	assert oct_res.shape == oct_buffer.shape
	assert not np.shares_memory(oct_res, oct_buffer)

	# Quaternion filter expects stride % 8 == 0 (typically 4x16-bit values).
	# We must allocate 32 bytes and pass stride=8 to prevent C++ heap overruns.
	quat_buffer = np.zeros(32, dtype=np.uint8)
	quat_res = decode_filter_quat(quat_buffer, 4, 8)
	assert quat_res.shape == quat_buffer.shape
	assert not np.shares_memory(quat_res, quat_buffer)

	# Exponential filter expects stride % 4 == 0 (16 bytes is safe for 4 count)
	exp_buffer = np.zeros(16, dtype=np.uint8)
	exp_res = decode_filter_exp(exp_buffer, 4, 4)
	assert exp_res.shape == exp_buffer.shape
	assert not np.shares_memory(exp_res, exp_buffer)

def test_encoding_decoding_runtime_errors(basic_mesh):
	"""Test that C++ failures properly trigger Python RuntimeErrors."""
	vertices, indices = basic_mesh

	# 1. Decode Errors: Corrupted/incomplete byte streams
	bad_data = b'\x00\x00\x00\x00'
	vertex_size = vertices.itemsize * vertices.shape[1]

	with pytest.raises(RuntimeError, match="Failed to decode vertex buffer"):
		decode_vertex_buffer(len(vertices), vertex_size, bad_data)

	with pytest.raises(RuntimeError, match="Failed to decode index buffer"):
		decode_index_buffer(len(indices), 4, bad_data)

	with pytest.raises(RuntimeError, match="Failed to decode index sequence"):
		decode_index_sequence(len(indices), 4, bad_data)

	# 2. Encode Errors: Simulating C++ failure (returning 0) via mocks
	with patch('utils.meshoptimizer.encoder.lib.meshopt_encodeVertexBuffer') as mock_enc_v:
		mock_enc_v.return_value = 0
		with pytest.raises(RuntimeError, match="Failed to encode vertex buffer"):
			encode_vertex_buffer(vertices)

	with patch('utils.meshoptimizer.encoder.lib.meshopt_encodeIndexBuffer') as mock_enc_i:
		mock_enc_i.return_value = 0
		with pytest.raises(RuntimeError, match="Failed to encode index buffer"):
			encode_index_buffer(indices)

	with patch('utils.meshoptimizer.encoder.lib.meshopt_encodeIndexSequence') as mock_enc_s:
		mock_enc_s.return_value = 0
		with pytest.raises(RuntimeError, match="Failed to encode index sequence"):
			encode_index_sequence(indices)
