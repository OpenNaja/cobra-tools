"""
Tests for the meshoptimizer Python wrapper.

This file contains tests to verify that the simplification functions
work correctly, evaluate attribute metrics, and appropriately default
when optional parameters are omitted.
"""
import numpy as np
import pytest
from utils.meshoptimizer import (
	simplify,
	simplify_with_attributes,
	simplify_sloppy,
	simplify_points,
	simplify_scale,
	SIMPLIFY_LOCK_BORDER,
	SIMPLIFY_SPARSE,
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

@pytest.fixture
def sphere_mesh():
	"""Generate a more complex mesh (a sphere with 8 segments and 8 rings)."""
	segments = 8
	rings = 8
	vertices = []
	indices = []

	for i in range(rings + 1):
		v = i / rings
		phi = v * np.pi

		for j in range(segments):
			u = j / segments
			theta = u * 2 * np.pi

			x = np.sin(phi) * np.cos(theta)
			y = np.sin(phi) * np.sin(theta)
			z = np.cos(phi)

			vertices.append([x, y, z])

	for i in range(rings):
		for j in range(segments):
			a = i * segments + j
			b = i * segments + (j + 1) % segments
			c = (i + 1) * segments + (j + 1) % segments
			d = (i + 1) * segments + j

			indices.extend([a, b, c])
			indices.extend([a, c, d])

	return np.array(vertices, dtype=np.float32), np.array(indices, dtype=np.uint32)


def test_simplify_basic(basic_mesh):
	"""Test basic simplification."""
	vertices, indices = basic_mesh
	simplified_indices = np.zeros_like(indices)
	result_error = np.array([0.0], dtype=np.float32)
	target_error = 0.01

	new_index_count = simplify(
		simplified_indices,
		indices,
		vertices,
		len(indices),
		len(vertices),
		vertices.itemsize * vertices.shape[1],
		len(indices) // 2,  # Target 50% reduction
		target_error,
		0,  # No options
		result_error
	)

	assert new_index_count <= len(indices)
	assert result_error[0] <= target_error

def test_simplify_with_attributes(basic_mesh):
	"""Test simplification utilizing external attribute matrices."""
	vertices, indices = basic_mesh
	simplified_indices = np.zeros_like(indices)
	result_error = np.array([0.0], dtype=np.float32)

	# Generate dummy attributes (e.g. vertex normals) and equal weights
	attributes = np.ones((len(vertices), 3), dtype=np.float32)
	weights = np.array([1.0, 1.0, 1.0], dtype=np.float32)

	new_index_count = simplify_with_attributes(
		simplified_indices,
		indices,
		vertices,
		attributes,
		weights,
		target_index_count=len(indices) // 2,
		result_error=result_error
	)

	assert new_index_count <= len(indices)
	assert result_error[0] >= 0.0

def test_simplify_options(basic_mesh):
	"""Test simplification with different options."""
	vertices, indices = basic_mesh

	# Test with SIMPLIFY_LOCK_BORDER option
	simplified_indices = np.zeros_like(indices)
	result_error = np.array([0.0], dtype=np.float32)

	new_index_count = simplify(
		simplified_indices,
		indices,
		vertices,
		len(indices),
		len(vertices),
		vertices.itemsize * vertices.shape[1],
		len(indices) // 2,
		0.01,
		SIMPLIFY_LOCK_BORDER,
		result_error
	)

	assert new_index_count <= len(indices)

	# Test with SIMPLIFY_SPARSE option
	simplified_indices = np.zeros_like(indices)
	result_error = np.array([0.0], dtype=np.float32)

	new_index_count = simplify(
		simplified_indices,
		indices,
		vertices,
		len(indices),
		len(vertices),
		vertices.itemsize * vertices.shape[1],
		len(indices) // 2,
		0.01,
		SIMPLIFY_SPARSE,
		result_error
	)

	assert new_index_count <= len(indices)

def test_simplify_sloppy(sphere_mesh):
	"""Test sloppy simplification."""
	sphere_vertices, sphere_indices = sphere_mesh

	simplified_indices = np.zeros_like(sphere_indices)
	result_error = np.array([0.0], dtype=np.float32)

	new_index_count = simplify_sloppy(
		simplified_indices,
		sphere_indices,
		sphere_vertices,
		len(sphere_indices),
		len(sphere_vertices),
		sphere_vertices.itemsize * sphere_vertices.shape[1],
		len(sphere_indices) // 4,  # Target 75% reduction
		0.01,  # Target error
		result_error
	)

	assert new_index_count <= len(sphere_indices)
	assert result_error[0] >= 0.0

def test_simplify_points():
	"""Test point cloud simplification."""
	points = np.random.rand(100, 3).astype(np.float32)
	simplified_points = np.zeros(50, dtype=np.uint32)

	new_point_count = simplify_points(
		simplified_points,
		points,
		None,  # No colors
		len(points),
		points.itemsize * points.shape[1],
		0,
		0.0,
		50  # Target 50% reduction
	)

	assert new_point_count <= 50

	# Test with colors
	colors = np.random.rand(100, 3).astype(np.float32)
	simplified_points = np.zeros(50, dtype=np.uint32)

	new_point_count = simplify_points(
		simplified_points,
		points,
		colors,
		len(points),
		points.itemsize * points.shape[1],
		colors.itemsize * colors.shape[1],
		1.0,
		50
	)

	assert new_point_count <= 50

def test_simplify_scale(basic_mesh):
	"""Test simplification scale calculation."""
	vertices, _ = basic_mesh

	scale = simplify_scale(
		vertices,
		len(vertices),
		vertices.itemsize * vertices.shape[1]
	)

	np.testing.assert_allclose(scale, 1.0, rtol=1e-7)

def test_simplifier_parameter_fallbacks(sphere_mesh):
	"""Test that missing arrays and arguments fall back safely."""
	sphere_vertices, sphere_indices = sphere_mesh
	simplified_indices = np.zeros_like(sphere_indices)

	expected_target = len(sphere_indices)

	new_count = simplify(simplified_indices, sphere_indices, sphere_vertices)
	assert new_count <= expected_target

	# Test simplify_sloppy without optional arguments + specific vertex_lock
	vertex_lock = np.zeros(len(sphere_vertices), dtype=np.uint8)
	vertex_lock[0] = 1 # Lock a single vertex

	new_sloppy_count = simplify_sloppy(
		simplified_indices,
		sphere_indices,
		sphere_vertices,
		vertex_lock=vertex_lock
	)
	assert new_sloppy_count > 0

	# Test simplify_with_attributes without optional arguments
	attributes = np.ones((len(sphere_vertices), 3), dtype=np.float32)
	weights = np.array([1.0, 1.0, 1.0], dtype=np.float32)

	new_attr_count = simplify_with_attributes(
		simplified_indices,
		sphere_indices,
		sphere_vertices,
		attributes,
		weights
	)
	assert new_attr_count > 0

	# Test simplify_points without optional arguments
	points = np.random.rand(50, 3).astype(np.float32)
	simplified_points = np.zeros(25, dtype=np.uint32)
	new_points_count = simplify_points(simplified_points, points)
	assert new_points_count > 0

	# Test simplify_scale without optional arguments
	scale = simplify_scale(sphere_vertices)
	assert scale > 0.0
