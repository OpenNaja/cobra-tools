"""
Tests for the meshoptimizer security limits.

Verifies that the validators correctly reject parameters that would cause
memory exhaustion or internal assertion failures in the C++ backend.
"""
import pytest
from utils.meshoptimizer.limits import MeshoptLimits

def test_validate_vertex_params_valid():
	"""Test that valid vertex parameters pass without raising exceptions."""
	MeshoptLimits.validate_vertex_params(vertex_count=100, vertex_size=12)
	MeshoptLimits.validate_vertex_params(vertex_count=0, vertex_size=4)

def test_validate_vertex_params_invalid():
	"""Test boundary limits and invalid logic for vertex parameter validation."""

	with pytest.raises(ValueError, match="non-negative"):
		MeshoptLimits.validate_vertex_params(vertex_count=-1, vertex_size=12)

	with pytest.raises(ValueError, match="positive"):
		MeshoptLimits.validate_vertex_params(vertex_count=100, vertex_size=0)

	with pytest.raises(ValueError, match="exceeds maximum"):
		# Maximum internal limit is 256
		MeshoptLimits.validate_vertex_params(vertex_count=100, vertex_size=260)

	with pytest.raises(ValueError, match="multiple of 4"):
		MeshoptLimits.validate_vertex_params(vertex_count=100, vertex_size=13)

	with pytest.raises(ValueError, match="exceeds maximum"):
		# Exceeds the max vertex count global variable
		MeshoptLimits.validate_vertex_params(
			vertex_count=MeshoptLimits.MAX_VERTEX_COUNT + 1,
			vertex_size=12
		)

	with pytest.raises(ValueError, match="exceeds limit"):
		# Exceeds the total allocated bytes limit without tripping MAX_VERTEX_COUNT
		# 90 million vertices * 12 bytes = 1.08 GB (> 1 GB limit)
		MeshoptLimits.validate_vertex_params(
			vertex_count=90_000_000,
			vertex_size=12
		)

def test_validate_index_params_valid():
	"""Test that valid index parameters pass without raising exceptions."""
	MeshoptLimits.validate_index_params(index_count=100, index_size=2)
	MeshoptLimits.validate_index_params(index_count=100, index_size=4)
	MeshoptLimits.validate_index_params(index_count=0, index_size=4)

def test_validate_index_params_invalid():
	"""Test boundary limits and invalid logic for index parameter validation."""

	with pytest.raises(ValueError, match="non-negative"):
		MeshoptLimits.validate_index_params(index_count=-1, index_size=4)

	with pytest.raises(ValueError, match="must be 2 or 4"):
		MeshoptLimits.validate_index_params(index_count=100, index_size=3)

	with pytest.raises(ValueError, match="exceeds maximum"):
		# Exceeds the max index count global variable
		MeshoptLimits.validate_index_params(
			index_count=MeshoptLimits.MAX_INDEX_COUNT + 1,
			index_size=4
		)

	with pytest.raises(ValueError, match="exceeds limit"):
		# Exceeds the total allocated bytes limit without tripping MAX_INDEX_COUNT
		# ~268.4 million indices * 4 bytes = ~1.07 GB (> 1 GB limit)
		MeshoptLimits.validate_index_params(
			index_count=MeshoptLimits.MAX_TOTAL_BYTES // 4 + 1,
			index_size=4
		)
