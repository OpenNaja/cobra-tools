"""
Tests for the meshoptimizer Python wrapper.

This file contains tests to verify that the meshlet generation, optimization,
and compression functions work correctly.
"""
import numpy as np
import pytest
from utils.meshoptimizer import (
	optimize_vertex_cache,
	optimize_vertex_fetch,
	build_meshlets_bound,
	build_meshlets,
	build_meshlets_scan,
	build_meshlets_flex,
	build_meshlets_spatial,
	optimize_meshlet,
	optimize_meshlet_level,
	compute_cluster_bounds,
	compute_meshlet_bounds,
	extract_meshlet_indices,
	encode_meshlet_bound,
	encode_meshlet,
	decode_meshlet,
	decode_meshlet_raw
)

def get_meshlet_triangles_set(mesh_v, mesh_t):
	triangles = set()
	for i in range(0, len(mesh_t), 3):
		g1 = mesh_v[mesh_t[i]]
		g2 = mesh_v[mesh_t[i+1]]
		g3 = mesh_v[mesh_t[i+2]]
		triangles.add(frozenset([g1, g2, g3]))
	return triangles

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

@pytest.fixture
def subdivided_cube_mesh():
	"""
	Generates a dense, highly subdivided cube mesh.
	Each of the 6 faces is divided into an (N x N) quad grid,
	resulting in a realistic topology for meshlet cluster testing.
	"""
	subdivisions = 8  # Number of segments per edge per face

	# The 6 faces of a cube defined by their 4 corner vertices
	# Winding orders match the original basic_mesh orientation
	face_corners = [
		# Front face (z = -0.5)
		[[-0.5, -0.5, -0.5], [ 0.5, -0.5, -0.5], [ 0.5,  0.5, -0.5], [-0.5,  0.5, -0.5]],
		# Right face (x = 0.5)
		[[ 0.5, -0.5, -0.5], [ 0.5, -0.5,  0.5], [ 0.5,  0.5,  0.5], [ 0.5,  0.5, -0.5]],
		# Back face (z = 0.5)
		[[ 0.5, -0.5,  0.5], [-0.5, -0.5,  0.5], [-0.5,  0.5,  0.5], [ 0.5,  0.5,  0.5]],
		# Left face (x = -0.5)
		[[-0.5, -0.5,  0.5], [-0.5, -0.5, -0.5], [-0.5,  0.5, -0.5], [-0.5,  0.5,  0.5]],
		# Top face (y = 0.5)
		[[-0.5,  0.5, -0.5], [ 0.5,  0.5, -0.5], [ 0.5,  0.5,  0.5], [-0.5,  0.5,  0.5]],
		# Bottom face (y = -0.5)
		[[-0.5, -0.5,  0.5], [ 0.5, -0.5,  0.5], [ 0.5, -0.5, -0.5], [-0.5, -0.5, -0.5]],
	]

	out_vertices = []
	out_indices = []
	vertex_count = 0

	# Linearly interpolate points across the surface of each face
	for face in face_corners:
		c00, c10, c11, c01 = [np.array(c, dtype=np.float32) for c in face]

		# Create a vertex mapping grid for the current face
		face_vertex_indices = np.zeros((subdivisions + 1, subdivisions + 1), dtype=np.uint32)

		for y in range(subdivisions + 1):
			v = y / subdivisions
			# Interpolate down left and right edges
			left_edge = (1.0 - v) * c00 + v * c01
			right_edge = (1.0 - v) * c10 + v * c11

			for x in range(subdivisions + 1):
				u = x / subdivisions
				# Interpolate across the row
				pos = (1.0 - u) * left_edge + u * right_edge

				out_vertices.append(pos)
				face_vertex_indices[y, x] = vertex_count
				vertex_count += 1

		# Generate triangles for the face grid cells
		for y in range(subdivisions):
			for x in range(subdivisions):
				i0 = face_vertex_indices[y, x]
				i1 = face_vertex_indices[y, x + 1]
				i2 = face_vertex_indices[y + 1, x + 1]
				i3 = face_vertex_indices[y + 1, x]

				# Maintain consistent winding order for the two triangles forming the quad
				out_indices.extend([i0, i1, i2])
				out_indices.extend([i0, i2, i3])

	# Convert lists into cohesive numpy arrays
	vertices = np.array(out_vertices, dtype=np.float32)
	indices = np.array(out_indices, dtype=np.uint32)

	return vertices, indices

@pytest.fixture
def optimized_cube(subdivided_cube_mesh):
	"""
	Pre-processes the mesh by optimizing vertex cache and fetch.
	Returns the optimized vertices and indices.
	"""
	vertices, indices = subdivided_cube_mesh
	index_count = len(indices)
	num_vertices = len(vertices)
	vertex_stride = vertices.itemsize * vertices.shape[1]

	# 1. Optimize Vertex Cache
	optimized_indices = np.empty_like(indices)
	optimize_vertex_cache(optimized_indices, indices, index_count, num_vertices)

	# 2. Optimize Vertex Fetch
	optimized_vertices = np.empty_like(vertices)

	unique_vertices = optimize_vertex_fetch(
		optimized_vertices,
		optimized_indices,
		vertices,
		index_count,
		num_vertices,
		vertex_stride
	)

	# Return the truncated unique vertices and the updated indices
	return optimized_vertices[:unique_vertices], optimized_indices

@pytest.fixture
def single_meshlet(optimized_cube):
	"""
	Builds meshlets from the optimized mesh and extracts the first one
	to provide a valid, realistic meshlet for downstream tests.
	"""
	vertices, indices = optimized_cube

	# Generate the meshlets
	meshlets, m_verts, m_tris = build_meshlets(
		indices,
		vertices,
		max_vertices=64,
		max_triangles=124
	)

	# Extract the first meshlet from the resulting arrays
	first_meshlet = meshlets[0]

	v_offset = first_meshlet['vertex_offset']
	v_count = first_meshlet['vertex_count']

	t_offset = first_meshlet['triangle_offset']
	t_count = first_meshlet['triangle_count']

	# Slice the exact local vertex and triangle data for this specific meshlet
	local_m_verts = m_verts[v_offset : v_offset + v_count]
	local_m_tris = m_tris[t_offset : t_offset + (t_count * 3)]

	# Pack it into a dictionary so tests have access to everything they need
	return {
		'global_vertices': vertices,
		'meshlet_vertices': local_m_verts,
		'meshlet_triangles': local_m_tris,
		'vertex_count': v_count,
		'triangle_count': t_count
	}

def test_build_meshlets_bound(subdivided_cube_mesh):
	"""Test that the maximum bound calculation returns a valid integer."""
	_, indices = subdivided_cube_mesh
	bound = build_meshlets_bound(len(indices), 64, 124)
	assert bound >= 38

def test_build_meshlets(optimized_cube):
	"""Test standard meshlet generation."""
	vertices, indices = optimized_cube
	meshlets, m_verts, m_tris = build_meshlets(
		indices, vertices, max_vertices=64, max_triangles=64
	)

	assert len(meshlets) == 12
	assert len(m_verts) == 564
	assert len(m_tris) == 2304
	assert 'vertex_offset' in meshlets.dtype.names

def test_build_meshlets_scan(optimized_cube):
	"""Test scan-based meshlet generation."""
	vertices, indices = optimized_cube
	meshlets, m_verts, m_tris = build_meshlets_scan(
		indices, len(vertices), max_vertices=64, max_triangles=64
	)

	assert len(meshlets) == 12
	assert len(m_verts) == 540
	assert len(m_tris) == 2304

def test_build_meshlets_flex(optimized_cube):
	"""Test flexible meshlet generation."""
	vertices, indices = optimized_cube
	meshlets, m_verts, m_tris = build_meshlets_flex(
		indices, vertices, max_vertices=64, min_triangles=32, max_triangles=64
	)

	assert len(meshlets) == 12
	assert len(m_verts) == 564
	assert len(m_tris) == 2304

def test_build_meshlets_spatial(optimized_cube):
	"""Test spatial layout meshlet generation."""
	vertices, indices = optimized_cube
	meshlets, m_verts, m_tris = build_meshlets_spatial(
		indices, vertices, max_vertices=64, min_triangles=32, max_triangles=64
	)

	assert len(meshlets) == 12
	assert len(m_verts) == 640
	assert len(m_tris) == 2304

def test_optimize_meshlet(single_meshlet):
	"""Test in-place meshlet optimization."""
	m_verts = single_meshlet['meshlet_vertices'].copy()
	m_tris = single_meshlet['meshlet_triangles'].copy()

	# Run the optimization (modifies arrays in-place)
	optimize_meshlet(
		m_verts,
		m_tris,
		triangle_count=single_meshlet['triangle_count'],
		vertex_count=single_meshlet['vertex_count']
	)

	# Ensure lengths are preserved
	assert len(m_verts) == len(single_meshlet['meshlet_vertices'])
	assert len(m_tris) == len(single_meshlet['meshlet_triangles'])

	# Ensure the exact same global vertices are present (even if reordered)
	assert np.array_equal(np.sort(m_verts), np.sort(single_meshlet['meshlet_vertices']))

	# Verify the global topology is preserved despite the local index scrambling
	orig_triangles = get_meshlet_triangles_set(single_meshlet['meshlet_vertices'], single_meshlet['meshlet_triangles'])
	opt_triangles = get_meshlet_triangles_set(m_verts, m_tris)

	assert orig_triangles == opt_triangles

def test_optimize_meshlet_level(single_meshlet):
	"""Test in-place meshlet level optimization."""
	m_verts = single_meshlet['meshlet_vertices'].copy()
	m_tris = single_meshlet['meshlet_triangles'].copy()

	# Modifies arrays in-place
	optimize_meshlet_level(
		m_verts,
		m_tris,
		triangle_count=single_meshlet['triangle_count'],
		vertex_count=single_meshlet['vertex_count'],
		level=5
	)

	assert len(m_verts) == len(single_meshlet['meshlet_vertices'])
	assert len(m_tris) == len(single_meshlet['meshlet_triangles'])

	assert np.array_equal(np.sort(m_verts), np.sort(single_meshlet['meshlet_vertices']))

	orig_triangles = get_meshlet_triangles_set(single_meshlet['meshlet_vertices'], single_meshlet['meshlet_triangles'])
	opt_triangles = get_meshlet_triangles_set(m_verts, m_tris)

	assert orig_triangles == opt_triangles

def test_compute_cluster_bounds(subdivided_cube_mesh):
	"""Test generation of bounds for a cluster."""
	vertices, indices = subdivided_cube_mesh
	# meshopt_computeClusterBounds expects a single cluster, not the whole mesh.
	# The C++ backend enforces a strict limit (kMeshletMaxTriangles, max 256).
	# We slice the first 128 triangles (384 indices) to safely simulate a cluster block.
	cluster_indices = indices[:384]

	bounds = compute_cluster_bounds(cluster_indices, vertices)

	assert isinstance(bounds, dict)
	assert 'center' in bounds
	assert 'radius' in bounds
	assert 'cone_apex' in bounds
	np.testing.assert_allclose(bounds['radius'], 0.707107, rtol=1e-6)

def test_compute_meshlet_bounds(single_meshlet):
	"""Test generation of bounds for a specific meshlet."""

	bounds = compute_meshlet_bounds(
		meshlet_vertices=single_meshlet['meshlet_vertices'],
		meshlet_triangles=single_meshlet['meshlet_triangles'],
		triangle_count=single_meshlet['triangle_count'],
		vertex_positions=single_meshlet['global_vertices']
	)

	assert isinstance(bounds, dict)
	assert 'center' in bounds
	assert 'radius' in bounds
	np.testing.assert_allclose(bounds['radius'], 0.707107, rtol=1e-6)

def test_extract_meshlet_indices(optimized_cube):
	"""Test extracting local indices from absolute index blocks."""
	_, indices = optimized_cube

	# Extract the first 4 triangles (12 indices)
	v, t = extract_meshlet_indices(indices[:12])

	assert len(v) <= 12
	assert len(t) == 12
	assert t.dtype == np.uint8
	assert v.dtype == np.uint32

def test_encode_decode_meshlet(single_meshlet):
	"""Test standard encoding and decoding compression loop."""
	v = single_meshlet['meshlet_vertices']
	t = single_meshlet['meshlet_triangles']

	bound = encode_meshlet_bound(len(v), len(t) // 3)
	assert bound > 0

	# Encode
	encoded = encode_meshlet(v, t)
	assert isinstance(encoded, bytes)
	assert len(encoded) > 0

	# Decode
	v_dec, t_dec = decode_meshlet(encoded, len(v), len(t) // 3)

	# Vertices should remain exactly identical
	np.testing.assert_array_equal(v, v_dec)

	# Triangles might be rotated by the encoder (e.g., [2, 3, 0] becomes [0, 2, 3]).
	# They preserve winding order, but direct array equality will fail.
	# We compare them as order-invariant sets of global index combinations.
	orig_triangles = get_meshlet_triangles_set(v, t)
	dec_triangles = get_meshlet_triangles_set(v_dec, t_dec)

	assert orig_triangles == dec_triangles

def test_decode_meshlet_raw(single_meshlet):
	"""Test SIMD-optimized raw meshlet decoding."""
	v = single_meshlet['meshlet_vertices']
	t = single_meshlet['meshlet_triangles']

	encoded = encode_meshlet(v, t)

	# Raw decoding returns triangles as packed 32-bit unsigned integers
	v_dec, t_dec = decode_meshlet_raw(encoded, len(v), len(t) // 3)

	np.testing.assert_array_equal(v, v_dec)

	# t_dec has one element per triangle (packed micro-indices)
	assert t_dec.dtype == np.uint32
	assert len(t_dec) == len(t) // 3
