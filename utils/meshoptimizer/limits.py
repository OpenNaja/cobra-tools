"""
Security limits and validation for meshoptimizer.

These limits prevent DoS attacks via memory exhaustion and ensure
parameters are valid before calling the C library.
"""


class MeshoptLimits:
    """
    Configurable security limits for meshoptimizer operations.

    Adjust these class variables to change limits globally:
        MeshoptLimits.MAX_TOTAL_BYTES = 2 * 1024 * 1024 * 1024  # 2 GB
    """

    # Maximum total bytes for any single allocation
    MAX_TOTAL_BYTES: int = 1 * 1024 * 1024 * 1024  # 1 GB

    # Maximum vertex size (meshoptimizer internal limit)
    MAX_VERTEX_SIZE: int = 256

    # Maximum vertex count
    MAX_VERTEX_COUNT: int = 100_000_000  # 100 million

    # Maximum index count
    MAX_INDEX_COUNT: int = 500_000_000  # 500 million (triangles * 3)

    @classmethod
    def validate_vertex_params(cls, vertex_count: int, vertex_size: int) -> None:
        """
        Validate vertex buffer parameters to prevent security issues.

        Args:
            vertex_count: Number of vertices
            vertex_size: Size of each vertex in bytes

        Raises:
            ValueError: If parameters are invalid or exceed limits
        """
        if vertex_count < 0:
            raise ValueError(f"vertex_count must be non-negative, got {vertex_count}")

        if vertex_size <= 0:
            raise ValueError(f"vertex_size must be positive, got {vertex_size}")

        if vertex_size > cls.MAX_VERTEX_SIZE:
            raise ValueError(f"vertex_size {vertex_size} exceeds maximum {cls.MAX_VERTEX_SIZE}")

        if vertex_size % 4 != 0:
            raise ValueError(
                f"vertex_size must be a multiple of 4, got {vertex_size}. "
                f"Consider using a dtype with itemsize >= 4 (e.g., float32, int32, float64)."
            )

        if vertex_count > cls.MAX_VERTEX_COUNT:
            raise ValueError(f"vertex_count {vertex_count} exceeds maximum {cls.MAX_VERTEX_COUNT}")

        total_bytes = vertex_count * vertex_size
        if total_bytes > cls.MAX_TOTAL_BYTES:
            raise ValueError(
                f"Requested allocation {total_bytes} bytes exceeds limit {cls.MAX_TOTAL_BYTES}"
            )

    @classmethod
    def validate_index_params(cls, index_count: int, index_size: int) -> None:
        """
        Validate index buffer parameters to prevent security issues.

        Args:
            index_count: Number of indices
            index_size: Size of each index in bytes (must be 2 or 4)

        Raises:
            ValueError: If parameters are invalid or exceed limits
        """
        if index_count < 0:
            raise ValueError(f"index_count must be non-negative, got {index_count}")

        if index_size not in (2, 4):
            raise ValueError(f"index_size must be 2 or 4, got {index_size}")

        if index_count > cls.MAX_INDEX_COUNT:
            raise ValueError(f"index_count {index_count} exceeds maximum {cls.MAX_INDEX_COUNT}")

        total_bytes = index_count * index_size
        if total_bytes > cls.MAX_TOTAL_BYTES:
            raise ValueError(
                f"Requested allocation {total_bytes} bytes exceeds limit {cls.MAX_TOTAL_BYTES}"
            )
