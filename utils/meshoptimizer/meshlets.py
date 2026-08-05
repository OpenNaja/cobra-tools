"""
Meshlet generation, optimization, and compression functions for meshoptimizer.
"""
import ctypes
from typing import Optional, Tuple, Dict, Any, Union
import numpy as np
from ._loader import lib, MeshoptBounds


# Define a matching numpy dtype for the meshopt_Meshlet struct
meshlet_dtype = np.dtype([
    ('vertex_offset', np.uint32),
    ('triangle_offset', np.uint32),
    ('vertex_count', np.uint32),
    ('triangle_count', np.uint32)
])


def _bounds_to_dict(bounds: MeshoptBounds) -> Dict[str, Any]:
    """Helper to convert the ctypes Bounds structure to a friendly Python dictionary."""
    return {
        "center": [bounds.center[0], bounds.center[1], bounds.center[2]],
        "radius": bounds.radius,
        "cone_apex": [bounds.cone_apex[0], bounds.cone_apex[1], bounds.cone_apex[2]],
        "cone_axis": [bounds.cone_axis[0], bounds.cone_axis[1], bounds.cone_axis[2]],
        "cone_cutoff": bounds.cone_cutoff,
        "cone_axis_s8": [bounds.cone_axis_s8[0], bounds.cone_axis_s8[1], bounds.cone_axis_s8[2]],
        "cone_cutoff_s8": bounds.cone_cutoff_s8
    }


def build_meshlets_bound(index_count: int, max_vertices: int, max_triangles: int) -> int:
    """
    Computes the maximum number of meshlets that could be generated.
    """
    return lib.meshopt_buildMeshletsBound(index_count, max_vertices, max_triangles)


def _trim_meshlet_arrays(meshlets: np.ndarray, meshlet_vertices: np.ndarray, 
                         meshlet_triangles: np.ndarray, count: int) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Helper to slice pre-allocated meshlet arrays down to their actual used sizes."""
    meshlets = meshlets[:count]
    if count > 0:
        last = meshlets[-1]
        # Arrays are populated contiguously; the total used items is the last meshlet's offset + its count
        meshlet_vertices = meshlet_vertices[:last['vertex_offset'] + last['vertex_count']]
        meshlet_triangles = meshlet_triangles[:last['triangle_offset'] + (last['triangle_count'] * 3)]
    else:
        meshlet_vertices = meshlet_vertices[:0]
        meshlet_triangles = meshlet_triangles[:0]
        
    return meshlets, meshlet_vertices, meshlet_triangles


def build_meshlets(indices: np.ndarray, vertex_positions: np.ndarray, 
                   max_vertices: int = 64, max_triangles: int = 124, 
                   cone_weight: float = 0.0) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Splits the mesh into a set of meshlets.
    """
    indices = np.asarray(indices, dtype=np.uint32)
    vertex_positions = np.asarray(vertex_positions, dtype=np.float32)
    index_count = len(indices)
    vertex_count = len(vertex_positions)
    vertex_positions_stride = vertex_positions.itemsize * vertex_positions.shape[1] if len(vertex_positions.shape) > 1 else vertex_positions.itemsize

    bound = build_meshlets_bound(index_count, max_vertices, max_triangles)

    meshlets = np.zeros(bound, dtype=meshlet_dtype)
    meshlet_vertices = np.zeros(index_count, dtype=np.uint32)
    meshlet_triangles = np.zeros(index_count, dtype=np.uint8)

    count = lib.meshopt_buildMeshlets(
        meshlets.ctypes.data_as(ctypes.c_void_p),
        meshlet_vertices.ctypes.data_as(ctypes.POINTER(ctypes.c_uint)),
        meshlet_triangles.ctypes.data_as(ctypes.POINTER(ctypes.c_ubyte)),
        indices.ctypes.data_as(ctypes.POINTER(ctypes.c_uint)),
        index_count,
        vertex_positions.ctypes.data_as(ctypes.POINTER(ctypes.c_float)),
        vertex_count,
        vertex_positions_stride,
        max_vertices,
        max_triangles,
        ctypes.c_float(cone_weight)
    )

    return _trim_meshlet_arrays(meshlets, meshlet_vertices, meshlet_triangles, count)


def build_meshlets_scan(indices: np.ndarray, vertex_count: Optional[int] = None, 
                        max_vertices: int = 64, max_triangles: int = 124) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Splits the mesh into a set of meshlets (scan mode without spatial info).
    For maximum efficiency the index buffer should be optimized for vertex cache first.
    """
    indices = np.asarray(indices, dtype=np.uint32)
    index_count = len(indices)
    if vertex_count is None:
        vertex_count = int(np.max(indices)) + 1 if index_count > 0 else 0

    bound = build_meshlets_bound(index_count, max_vertices, max_triangles)

    meshlets = np.zeros(bound, dtype=meshlet_dtype)
    meshlet_vertices = np.zeros(index_count, dtype=np.uint32)
    meshlet_triangles = np.zeros(index_count, dtype=np.uint8)

    count = lib.meshopt_buildMeshletsScan(
        meshlets.ctypes.data_as(ctypes.c_void_p),
        meshlet_vertices.ctypes.data_as(ctypes.POINTER(ctypes.c_uint)),
        meshlet_triangles.ctypes.data_as(ctypes.POINTER(ctypes.c_ubyte)),
        indices.ctypes.data_as(ctypes.POINTER(ctypes.c_uint)),
        index_count,
        vertex_count,
        max_vertices,
        max_triangles
    )

    return _trim_meshlet_arrays(meshlets, meshlet_vertices, meshlet_triangles, count)


def build_meshlets_flex(indices: np.ndarray, vertex_positions: np.ndarray, 
                        max_vertices: int = 64, min_triangles: int = 32, max_triangles: int = 124, 
                        cone_weight: float = 0.0, split_factor: float = 0.5) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Splits the mesh into a set of meshlets allowing flexibility for cluster sizes.
    """
    indices = np.asarray(indices, dtype=np.uint32)
    vertex_positions = np.asarray(vertex_positions, dtype=np.float32)
    index_count = len(indices)
    vertex_count = len(vertex_positions)
    vertex_positions_stride = vertex_positions.itemsize * vertex_positions.shape[1] if len(vertex_positions.shape) > 1 else vertex_positions.itemsize

    bound = build_meshlets_bound(index_count, max_vertices, min_triangles)

    meshlets = np.zeros(bound, dtype=meshlet_dtype)
    meshlet_vertices = np.zeros(index_count, dtype=np.uint32)
    meshlet_triangles = np.zeros(index_count, dtype=np.uint8)

    count = lib.meshopt_buildMeshletsFlex(
        meshlets.ctypes.data_as(ctypes.c_void_p),
        meshlet_vertices.ctypes.data_as(ctypes.POINTER(ctypes.c_uint)),
        meshlet_triangles.ctypes.data_as(ctypes.POINTER(ctypes.c_ubyte)),
        indices.ctypes.data_as(ctypes.POINTER(ctypes.c_uint)),
        index_count,
        vertex_positions.ctypes.data_as(ctypes.POINTER(ctypes.c_float)),
        vertex_count,
        vertex_positions_stride,
        max_vertices,
        min_triangles,
        max_triangles,
        ctypes.c_float(cone_weight),
        ctypes.c_float(split_factor)
    )

    return _trim_meshlet_arrays(meshlets, meshlet_vertices, meshlet_triangles, count)


def build_meshlets_spatial(indices: np.ndarray, vertex_positions: np.ndarray, 
                           max_vertices: int = 64, min_triangles: int = 32, max_triangles: int = 124, 
                           fill_weight: float = 0.5) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Splits the mesh into meshlets optimized for raytracing spatial layout.
    """
    indices = np.asarray(indices, dtype=np.uint32)
    vertex_positions = np.asarray(vertex_positions, dtype=np.float32)
    index_count = len(indices)
    vertex_count = len(vertex_positions)
    vertex_positions_stride = vertex_positions.itemsize * vertex_positions.shape[1] if len(vertex_positions.shape) > 1 else vertex_positions.itemsize

    bound = build_meshlets_bound(index_count, max_vertices, min_triangles)

    meshlets = np.zeros(bound, dtype=meshlet_dtype)
    meshlet_vertices = np.zeros(index_count, dtype=np.uint32)
    meshlet_triangles = np.zeros(index_count, dtype=np.uint8)

    count = lib.meshopt_buildMeshletsSpatial(
        meshlets.ctypes.data_as(ctypes.c_void_p),
        meshlet_vertices.ctypes.data_as(ctypes.POINTER(ctypes.c_uint)),
        meshlet_triangles.ctypes.data_as(ctypes.POINTER(ctypes.c_ubyte)),
        indices.ctypes.data_as(ctypes.POINTER(ctypes.c_uint)),
        index_count,
        vertex_positions.ctypes.data_as(ctypes.POINTER(ctypes.c_float)),
        vertex_count,
        vertex_positions_stride,
        max_vertices,
        min_triangles,
        max_triangles,
        ctypes.c_float(fill_weight)
    )

    return _trim_meshlet_arrays(meshlets, meshlet_vertices, meshlet_triangles, count)


def optimize_meshlet(meshlet_vertices: np.ndarray, meshlet_triangles: np.ndarray, 
                     triangle_count: int, vertex_count: int) -> None:
    """
    Reorders meshlet vertices and triangles to maximize locality. Modifies inputs in-place.
    """
    lib.meshopt_optimizeMeshlet(
        meshlet_vertices.ctypes.data_as(ctypes.POINTER(ctypes.c_uint)),
        meshlet_triangles.ctypes.data_as(ctypes.POINTER(ctypes.c_ubyte)),
        triangle_count,
        vertex_count
    )


def optimize_meshlet_level(meshlet_vertices: np.ndarray, meshlet_triangles: np.ndarray, 
                           triangle_count: int, vertex_count: int, level: int = 3) -> None:
    """
    Reorders meshlet to maximize locality with different levels of aggressiveness. Modifies inputs in-place.
    Note: level ranges from [0, 9]. Higher is slower but yields better compression.
    """
    lib.meshopt_optimizeMeshletLevel(
        meshlet_vertices.ctypes.data_as(ctypes.POINTER(ctypes.c_uint)),
        vertex_count,
        meshlet_triangles.ctypes.data_as(ctypes.POINTER(ctypes.c_ubyte)),
        triangle_count,
        level
    )


def compute_cluster_bounds(indices: np.ndarray, vertex_positions: np.ndarray, 
                           vertex_positions_stride: Optional[int] = None) -> Dict[str, Any]:
    """
    Creates bounding volumes for frustum, backface, and occlusion culling of an index block.
    """
    indices = np.asarray(indices, dtype=np.uint32)
    vertex_positions = np.asarray(vertex_positions, dtype=np.float32)
    index_count = len(indices)
    vertex_count = len(vertex_positions)

    if vertex_positions_stride is None:
        vertex_positions_stride = vertex_positions.itemsize * vertex_positions.shape[1] if len(vertex_positions.shape) > 1 else vertex_positions.itemsize

    bounds = lib.meshopt_computeClusterBounds(
        indices.ctypes.data_as(ctypes.POINTER(ctypes.c_uint)),
        index_count,
        vertex_positions.ctypes.data_as(ctypes.POINTER(ctypes.c_float)),
        vertex_count,
        vertex_positions_stride
    )

    return _bounds_to_dict(bounds)


def compute_meshlet_bounds(meshlet_vertices: np.ndarray, meshlet_triangles: np.ndarray, 
                           triangle_count: int, vertex_positions: np.ndarray, 
                           vertex_positions_stride: Optional[int] = None) -> Dict[str, Any]:
    """
    Creates bounding volumes for frustum, backface, and occlusion culling of a specific meshlet.
    """
    meshlet_vertices = np.asarray(meshlet_vertices, dtype=np.uint32)
    meshlet_triangles = np.asarray(meshlet_triangles, dtype=np.uint8)
    vertex_positions = np.asarray(vertex_positions, dtype=np.float32)
    vertex_count = len(vertex_positions)
    
    if vertex_positions_stride is None:
        vertex_positions_stride = vertex_positions.itemsize * vertex_positions.shape[1] if len(vertex_positions.shape) > 1 else vertex_positions.itemsize

    bounds = lib.meshopt_computeMeshletBounds(
        meshlet_vertices.ctypes.data_as(ctypes.POINTER(ctypes.c_uint)),
        meshlet_triangles.ctypes.data_as(ctypes.POINTER(ctypes.c_ubyte)),
        triangle_count,
        vertex_positions.ctypes.data_as(ctypes.POINTER(ctypes.c_float)),
        vertex_count,
        vertex_positions_stride
    )

    return _bounds_to_dict(bounds)


def extract_meshlet_indices(indices: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """
    Extract meshlet-local vertex and triangle indices from absolute cluster indices.
    """
    indices = np.asarray(indices, dtype=np.uint32)
    index_count = len(indices)

    # Max allowed by meshoptimizer is 256
    vertices = np.zeros(256, dtype=np.uint32)
    triangles = np.zeros(index_count, dtype=np.uint8)

    vertex_count = lib.meshopt_extractMeshletIndices(
        vertices.ctypes.data_as(ctypes.POINTER(ctypes.c_uint)),
        triangles.ctypes.data_as(ctypes.POINTER(ctypes.c_ubyte)),
        indices.ctypes.data_as(ctypes.POINTER(ctypes.c_uint)),
        index_count
    )

    return vertices[:vertex_count], triangles


def encode_meshlet_bound(max_vertices: int, max_triangles: int) -> int:
    """
    Computes the worst-case size for encoded meshlet data.
    """
    return lib.meshopt_encodeMeshletBound(max_vertices, max_triangles)


def encode_meshlet(vertices: Optional[np.ndarray], triangles: np.ndarray) -> bytes:
    """
    Encodes meshlet data into a smaller byte array.
    """
    vertices = np.asarray(vertices, dtype=np.uint32) if vertices is not None else None
    triangles = np.asarray(triangles, dtype=np.uint8)
    
    vertex_count = len(vertices) if vertices is not None else 0
    triangle_count = len(triangles) // 3

    bound = lib.meshopt_encodeMeshletBound(vertex_count, triangle_count)
    buffer = np.zeros(bound, dtype=np.uint8)

    result_size = lib.meshopt_encodeMeshlet(
        buffer.ctypes.data_as(ctypes.POINTER(ctypes.c_ubyte)),
        bound,
        vertices.ctypes.data_as(ctypes.POINTER(ctypes.c_uint)) if vertices is not None else None,
        vertex_count,
        triangles.ctypes.data_as(ctypes.POINTER(ctypes.c_ubyte)),
        triangle_count
    )

    if result_size == 0:
        raise RuntimeError("Failed to encode meshlet (buffer size too small or invalid input).")

    return bytes(buffer[:result_size])


def decode_meshlet(buffer: Union[bytes, np.ndarray], vertex_count: int, triangle_count: int, 
                   vertex_size: int = 4, triangle_size: int = 3) -> Tuple[np.ndarray, np.ndarray]:
    """
    Decodes meshlet data from an array of bytes.
    vertex_size: 2 (16-bit) or 4 (32-bit).
    triangle_size: 3 (8-bit micro indices) or 4 (32-bit packed).
    """
    buffer_array = np.frombuffer(buffer, dtype=np.uint8)
    
    if vertex_size == 4:
        vertices = np.zeros(vertex_count, dtype=np.uint32)
    elif vertex_size == 2:
        vertices = np.zeros(vertex_count, dtype=np.uint16)
    else:
        raise ValueError("vertex_size must be 2 or 4")

    # The resulting buffers need to be 4-byte aligned due to SIMD decoding requirements sometimes under the hood
    if triangle_size == 3:
        triangles = np.zeros((triangle_count * 3 + 3) & ~3, dtype=np.uint8)
    elif triangle_size == 4:
        triangles = np.zeros(triangle_count, dtype=np.uint32)
    else:
        raise ValueError("triangle_size must be 3 or 4")

    result = lib.meshopt_decodeMeshlet(
        vertices.ctypes.data_as(ctypes.c_void_p),
        vertex_count,
        vertex_size,
        triangles.ctypes.data_as(ctypes.c_void_p),
        triangle_count,
        triangle_size,
        buffer_array.ctypes.data_as(ctypes.POINTER(ctypes.c_ubyte)),
        len(buffer_array)
    )

    if result != 0:
        raise RuntimeError(f"Failed to decode meshlet: error code {result}")

    # Trim any required padding
    if triangle_size == 3:
        triangles = triangles[:triangle_count * 3]

    return vertices, triangles


def decode_meshlet_raw(buffer: Union[bytes, np.ndarray], vertex_count: int, triangle_count: int) -> Tuple[np.ndarray, np.ndarray]:
    """
    "Raw" decoding for meshlets (SIMD optimized extraction directly to 32-bit targets).
    The outputs arrays will be safely memory-aligned behind the scenes.
    """
    buffer_array = np.frombuffer(buffer, dtype=np.uint8)
    
    # Needs to be 16-byte aligned for raw mode. We allocate slightly larger buffers.
    v_elements = (vertex_count + 3) & ~3 
    t_elements = (triangle_count + 3) & ~3 

    vertices = np.zeros(max(v_elements, 4), dtype=np.uint32) 
    triangles = np.zeros(max(t_elements, 4), dtype=np.uint32)

    result = lib.meshopt_decodeMeshletRaw(
        vertices.ctypes.data_as(ctypes.POINTER(ctypes.c_uint)),
        vertex_count,
        triangles.ctypes.data_as(ctypes.POINTER(ctypes.c_uint)),
        triangle_count,
        buffer_array.ctypes.data_as(ctypes.POINTER(ctypes.c_ubyte)),
        len(buffer_array)
    )

    if result != 0:
        raise RuntimeError(f"Failed to decode raw meshlet: error code {result}")

    return vertices[:vertex_count], triangles[:triangle_count]
