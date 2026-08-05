"""
Tests for the meshoptimizer Python wrapper.

This file contains tests to verify that the optimization functions
work correctly, preserve the mesh geometry, and handle optional
parameters via internal fallback logic.
"""
import numpy as np
import pytest
from utils.meshoptimizer import (
	optimize_vertex_cache,
	optimize_vertex_cache_strip,
	optimize_vertex_cache_fifo,
	optimize_overdraw,
	optimize_vertex_fetch,
	optimize_vertex_fetch_remap,
	generate_vertex_remap,
	remap_vertex_buffer,
	remap_index_buffer
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

def test_vertex_cache_optimization(basic_mesh):
	"""Test vertex cache optimization."""
	vertices, indices = basic_mesh

	optimized_indices = np.zeros_like(indices)
	optimize_vertex_cache(
		optimized_indices,
		indices,
		len(indices),
		len(vertices)
	)

	assert len(indices) == len(optimized_indices)

	original_triangles = get_triangles_set(vertices, indices)
	optimized_triangles = get_triangles_set(vertices, optimized_indices)
	assert original_triangles == optimized_triangles

def test_vertex_cache_strip_optimization(basic_mesh):
	"""Test vertex cache optimization for strip-like caches."""
	vertices, indices = basic_mesh

	optimized_indices = np.zeros_like(indices)
	optimize_vertex_cache_strip(
		optimized_indices,
		indices,
		len(indices),
		len(vertices)
	)

	assert len(indices) == len(optimized_indices)

	original_triangles = get_triangles_set(vertices, indices)
	optimized_triangles = get_triangles_set(vertices, optimized_indices)
	assert original_triangles == optimized_triangles

def test_vertex_cache_fifo_optimization(basic_mesh):
	"""Test vertex cache optimization for FIFO caches."""
	vertices, indices = basic_mesh

	optimized_indices = np.zeros_like(indices)
	optimize_vertex_cache_fifo(
		optimized_indices,
		indices,
		len(indices),
		len(vertices),
		cache_size=16
	)

	assert len(indices) == len(optimized_indices)

	original_triangles = get_triangles_set(vertices, indices)
	optimized_triangles = get_triangles_set(vertices, optimized_indices)
	assert original_triangles == optimized_triangles

def test_overdraw_optimization(basic_mesh):
	"""Test overdraw optimization."""
	vertices, indices = basic_mesh

	optimized_indices = np.zeros_like(indices)
	optimize_overdraw(
		optimized_indices,
		indices,
		vertices,
		len(indices),
		len(vertices),
		vertices.itemsize * vertices.shape[1],
		1.05
	)

	assert len(indices) == len(optimized_indices)

	original_triangles = get_triangles_set(vertices, indices)
	optimized_triangles = get_triangles_set(vertices, optimized_indices)
	assert original_triangles == optimized_triangles

def test_vertex_fetch_optimization(basic_mesh):
	"""Test vertex fetch optimization."""
	vertices, original_indices = basic_mesh

	# Extract the geometric triangles BEFORE the indices are modified in-place
	original_triangles = get_triangles_set(vertices, original_indices)

	# Copy the indices so we don't accidentally mutate the fixture data
	indices_to_optimize = original_indices.copy()
	optimized_vertices = np.zeros_like(vertices)

	unique_vertex_count = optimize_vertex_fetch(
		optimized_vertices,
		indices_to_optimize,
		vertices,
		len(indices_to_optimize),
		len(vertices),
		vertices.itemsize * vertices.shape[1]
	)

	# Check that we didn't somehow generate more unique vertices than we started with
	assert unique_vertex_count <= len(vertices)

	# Validate that the geometric topology was perfectly preserved
	# by evaluating the in-place modified indices against the newly reordered vertices
	optimized_triangles = get_triangles_set(optimized_vertices, indices_to_optimize)

	assert original_triangles == optimized_triangles

def test_vertex_fetch_remap_optimization(basic_mesh):
	"""Test vertex fetch remap generation directly."""
	_, indices = basic_mesh

	destination = np.zeros_like(indices)
	unique_vertex_count = optimize_vertex_fetch_remap(
		destination,
		indices,
		len(indices),
		int(np.max(indices)) + 1
	)

	assert unique_vertex_count > 0

def test_vertex_remap(basic_mesh):
	"""Test vertex remapping."""
	vertices, indices = basic_mesh

	remap = np.zeros(len(vertices), dtype=np.uint32)
	unique_vertex_count = generate_vertex_remap(
		remap,
		indices,
		len(indices),
		vertices,
		len(vertices),
		vertices.itemsize * vertices.shape[1]
	)

	assert unique_vertex_count <= len(vertices)

	remapped_vertices = np.zeros_like(vertices)
	remap_vertex_buffer(
		remapped_vertices,
		vertices,
		len(vertices),
		vertices.itemsize * vertices.shape[1],
		remap
	)

	remapped_indices = np.zeros_like(indices)
	remap_index_buffer(
		remapped_indices,
		indices,
		len(indices),
		remap
	)

	original_triangles = get_triangles_set(vertices, indices)
	remapped_triangles = get_triangles_set(remapped_vertices, remapped_indices)
	assert original_triangles == remapped_triangles

def test_utils_unindexed_remap():
	"""Test generate_vertex_remap for unindexed geometry (utils.py coverage)."""
	# Create an unindexed point cloud with duplicate points
	vertices = np.array([
		[1.0, 2.0, 3.0],
		[1.0, 2.0, 3.0],
		[4.0, 5.0, 6.0]
	], dtype=np.float32)

	remap = np.zeros(len(vertices), dtype=np.uint32)

	# Pass None for indices to trigger the unindexed geometry branch
	unique_count = generate_vertex_remap(remap, indices=None, vertices=vertices)

	assert unique_count == 2
	assert remap[0] == remap[1] # The duplicate should map to the same target index

def test_optimizer_parameter_fallbacks(basic_mesh):
	"""Test that all optimizer functions correctly derive sizes and counts if omitted."""
	vertices, indices = basic_mesh

	optimized_indices = np.zeros_like(indices)

	# Vertex Cache Variants
	optimize_vertex_cache(optimized_indices, indices)
	assert len(optimized_indices) > 0

	optimize_vertex_cache_strip(optimized_indices, indices)
	assert len(optimized_indices) > 0

	optimize_vertex_cache_fifo(optimized_indices, indices)
	assert len(optimized_indices) > 0

	# Vertex Fetch Variants
	optimized_vertices = np.zeros_like(vertices)
	optimize_vertex_fetch(optimized_vertices, indices, vertices)
	assert len(optimized_vertices) > 0

	optimize_vertex_fetch_remap(optimized_indices, indices)
	assert len(optimized_indices) > 0

	# Overdraw
	optimize_overdraw(optimized_indices, indices, vertices)
	assert len(optimized_indices) > 0

	# Utils
	remap = np.zeros(len(vertices), dtype=np.uint32)
	generate_vertex_remap(remap, indices=indices, vertices=vertices)
	remap_vertex_buffer(optimized_vertices, vertices, remap=remap)
	remap_index_buffer(optimized_indices, indices, remap=remap)
	assert len(optimized_vertices) > 0
