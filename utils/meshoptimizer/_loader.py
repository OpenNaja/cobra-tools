"""
Library loader for meshoptimizer.
"""
import ctypes
import os
import sys
import platform
import glob
from typing import Optional, List, Any
import numpy as np


class MeshoptBounds(ctypes.Structure):
    _fields_ = [
        ("center", ctypes.c_float * 3),
        ("radius", ctypes.c_float),
        ("cone_apex", ctypes.c_float * 3),
        ("cone_axis", ctypes.c_float * 3),
        ("cone_cutoff", ctypes.c_float),
        ("cone_axis_s8", ctypes.c_int8 * 3),
        ("cone_cutoff_s8", ctypes.c_int8),
    ]


def find_library() -> str:
    """Find the meshoptimizer shared library."""
    this_dir = os.path.dirname(os.path.abspath(__file__))
    if platform.system() == 'Windows':
        pattern = os.path.join(this_dir, 'meshoptimizer.dll')
    else:
        pattern = os.path.join(this_dir, '*meshoptimizer*.so')

    lib_files = glob.glob(pattern)
    if lib_files:
        return lib_files[0]

    raise ImportError(f"Could not find meshoptimizer library in {this_dir}")

# Load the library
try:
    lib_path = find_library()
    lib = ctypes.CDLL(lib_path)
except ImportError as e:
    print(f"Error loading meshoptimizer library: {e}")
    print("Make sure the library is properly installed.")
    raise

# Define function signatures
def setup_function_signatures() -> None:
    """Set up the function signatures for the library."""
    # Vertex remap functions
    lib.meshopt_generateVertexRemap.argtypes = [
        ctypes.POINTER(ctypes.c_uint),  # destination
        ctypes.POINTER(ctypes.c_uint),  # indices
        ctypes.c_size_t,                # index_count
        ctypes.c_void_p,                # vertices
        ctypes.c_size_t,                # vertex_count
        ctypes.c_size_t                 # vertex_size
    ]
    lib.meshopt_generateVertexRemap.restype = ctypes.c_size_t

    lib.meshopt_remapVertexBuffer.argtypes = [
        ctypes.c_void_p,                # destination
        ctypes.c_void_p,                # vertices
        ctypes.c_size_t,                # vertex_count
        ctypes.c_size_t,                # vertex_size
        ctypes.POINTER(ctypes.c_uint)   # remap
    ]
    lib.meshopt_remapVertexBuffer.restype = None

    lib.meshopt_remapIndexBuffer.argtypes = [
        ctypes.POINTER(ctypes.c_uint),  # destination
        ctypes.POINTER(ctypes.c_uint),  # indices
        ctypes.c_size_t,                # index_count
        ctypes.POINTER(ctypes.c_uint)   # remap
    ]
    lib.meshopt_remapIndexBuffer.restype = None

    # Vertex cache optimization
    lib.meshopt_optimizeVertexCache.argtypes = [
        ctypes.POINTER(ctypes.c_uint),  # destination
        ctypes.POINTER(ctypes.c_uint),  # indices
        ctypes.c_size_t,                # index_count
        ctypes.c_size_t                 # vertex_count
    ]
    lib.meshopt_optimizeVertexCache.restype = None

    # Overdraw optimization
    lib.meshopt_optimizeOverdraw.argtypes = [
        ctypes.POINTER(ctypes.c_uint),  # destination
        ctypes.POINTER(ctypes.c_uint),  # indices
        ctypes.c_size_t,                # index_count
        ctypes.POINTER(ctypes.c_float), # vertex_positions
        ctypes.c_size_t,                # vertex_count
        ctypes.c_size_t,                # vertex_positions_stride
        ctypes.c_float                  # threshold
    ]
    lib.meshopt_optimizeOverdraw.restype = None

    # Vertex fetch optimization
    lib.meshopt_optimizeVertexFetch.argtypes = [
        ctypes.c_void_p,                # destination
        ctypes.POINTER(ctypes.c_uint),  # indices
        ctypes.c_size_t,                # index_count
        ctypes.c_void_p,                # vertices
        ctypes.c_size_t,                # vertex_count
        ctypes.c_size_t                 # vertex_size
    ]
    lib.meshopt_optimizeVertexFetch.restype = ctypes.c_size_t


    # Decoder Filters
    lib.meshopt_decodeFilterOct.argtypes = [
        ctypes.c_void_p,                # buffer
        ctypes.c_size_t,                # count
        ctypes.c_size_t                 # stride
    ]
    lib.meshopt_decodeFilterOct.restype = None

    lib.meshopt_decodeFilterQuat.argtypes = [
        ctypes.c_void_p,                # buffer
        ctypes.c_size_t,                # count
        ctypes.c_size_t                 # stride
    ]
    lib.meshopt_decodeFilterQuat.restype = None

    lib.meshopt_decodeFilterExp.argtypes = [
        ctypes.c_void_p,                # buffer
        ctypes.c_size_t,                # count
        ctypes.c_size_t                 # stride
    ]
    lib.meshopt_decodeFilterExp.restype = None

    # Additional Optimizers
    lib.meshopt_optimizeVertexCacheStrip.argtypes = [
        ctypes.POINTER(ctypes.c_uint),  # destination
        ctypes.POINTER(ctypes.c_uint),  # indices
        ctypes.c_size_t,                # index_count
        ctypes.c_size_t                 # vertex_count
    ]
    lib.meshopt_optimizeVertexCacheStrip.restype = None

    lib.meshopt_optimizeVertexCacheFifo.argtypes = [
        ctypes.POINTER(ctypes.c_uint),  # destination
        ctypes.POINTER(ctypes.c_uint),  # indices
        ctypes.c_size_t,                # index_count
        ctypes.c_size_t,                # vertex_count
        ctypes.c_uint                   # cache_size
    ]
    lib.meshopt_optimizeVertexCacheFifo.restype = None

    lib.meshopt_optimizeVertexFetchRemap.argtypes = [
        ctypes.POINTER(ctypes.c_uint),  # destination
        ctypes.POINTER(ctypes.c_uint),  # indices
        ctypes.c_size_t,                # index_count
        ctypes.c_size_t                 # vertex_count
    ]
    lib.meshopt_optimizeVertexFetchRemap.restype = ctypes.c_size_t

    # Simplification
    lib.meshopt_simplify.argtypes = [
        ctypes.POINTER(ctypes.c_uint),  # destination
        ctypes.POINTER(ctypes.c_uint),  # indices
        ctypes.c_size_t,                # index_count
        ctypes.POINTER(ctypes.c_float), # vertex_positions
        ctypes.c_size_t,                # vertex_count
        ctypes.c_size_t,                # vertex_positions_stride
        ctypes.c_size_t,                # target_index_count
        ctypes.c_float,                 # target_error
        ctypes.c_uint,                  # options
        ctypes.POINTER(ctypes.c_float)  # result_error
    ]
    lib.meshopt_simplify.restype = ctypes.c_size_t

    # Simplification scale
    lib.meshopt_simplifyScale.argtypes = [
        ctypes.POINTER(ctypes.c_float), # vertex_positions
        ctypes.c_size_t,                # vertex_count
        ctypes.c_size_t                 # vertex_positions_stride
    ]
    lib.meshopt_simplifyScale.restype = ctypes.c_float  # Return type is float

    # Encoding
    lib.meshopt_encodeVertexBufferBound.argtypes = [
        ctypes.c_size_t,                # vertex_count
        ctypes.c_size_t                 # vertex_size
    ]
    lib.meshopt_encodeVertexBufferBound.restype = ctypes.c_size_t

    lib.meshopt_encodeVertexBuffer.argtypes = [
        ctypes.POINTER(ctypes.c_ubyte), # buffer
        ctypes.c_size_t,                # buffer_size
        ctypes.c_void_p,                # vertices
        ctypes.c_size_t,                # vertex_count
        ctypes.c_size_t                 # vertex_size
    ]
    lib.meshopt_encodeVertexBuffer.restype = ctypes.c_size_t

    lib.meshopt_encodeIndexBufferBound.argtypes = [
        ctypes.c_size_t,                # index_count
        ctypes.c_size_t                 # vertex_count
    ]
    lib.meshopt_encodeIndexBufferBound.restype = ctypes.c_size_t

    lib.meshopt_encodeIndexBuffer.argtypes = [
        ctypes.POINTER(ctypes.c_ubyte), # buffer
        ctypes.c_size_t,                # buffer_size
        ctypes.POINTER(ctypes.c_uint),  # indices
        ctypes.c_size_t                 # index_count
    ]
    lib.meshopt_encodeIndexBuffer.restype = ctypes.c_size_t

    lib.meshopt_encodeIndexSequenceBound.argtypes = [
        ctypes.c_size_t,                # index_count
        ctypes.c_size_t                 # vertex_count
    ]
    lib.meshopt_encodeIndexSequenceBound.restype = ctypes.c_size_t

    lib.meshopt_encodeIndexSequence.argtypes = [
        ctypes.POINTER(ctypes.c_ubyte), # buffer
        ctypes.c_size_t,                # buffer_size
        ctypes.POINTER(ctypes.c_uint),  # indices
        ctypes.c_size_t                 # index_count
    ]
    lib.meshopt_encodeIndexSequence.restype = ctypes.c_size_t

    # Decoding
    lib.meshopt_decodeVertexBuffer.argtypes = [
        ctypes.c_void_p,                # destination
        ctypes.c_size_t,                # vertex_count
        ctypes.c_size_t,                # vertex_size
        ctypes.POINTER(ctypes.c_ubyte), # buffer
        ctypes.c_size_t                 # buffer_size
    ]
    lib.meshopt_decodeVertexBuffer.restype = ctypes.c_int

    lib.meshopt_decodeIndexBuffer.argtypes = [
        ctypes.c_void_p,                # destination
        ctypes.c_size_t,                # index_count
        ctypes.c_size_t,                # index_size
        ctypes.POINTER(ctypes.c_ubyte), # buffer
        ctypes.c_size_t                 # buffer_size
    ]
    lib.meshopt_decodeIndexBuffer.restype = ctypes.c_int

    lib.meshopt_decodeIndexSequence.argtypes = [
        ctypes.c_void_p,                # destination
        ctypes.c_size_t,                # index_count
        ctypes.c_size_t,                # index_size
        ctypes.POINTER(ctypes.c_ubyte), # buffer
        ctypes.c_size_t                 # buffer_size
    ]
    lib.meshopt_decodeIndexSequence.restype = ctypes.c_int

    # Encoding/Decoding versions
    lib.meshopt_encodeVertexVersion.argtypes = [ctypes.c_int]
    lib.meshopt_encodeVertexVersion.restype = None

    lib.meshopt_encodeIndexVersion.argtypes = [ctypes.c_int]
    lib.meshopt_encodeIndexVersion.restype = None

    lib.meshopt_decodeVertexVersion.argtypes = [
        ctypes.POINTER(ctypes.c_ubyte), # buffer
        ctypes.c_size_t                 # buffer_size
    ]
    lib.meshopt_decodeVertexVersion.restype = ctypes.c_int

    lib.meshopt_decodeIndexVersion.argtypes = [
        ctypes.POINTER(ctypes.c_ubyte), # buffer
        ctypes.c_size_t                 # buffer_size
    ]
    lib.meshopt_decodeIndexVersion.restype = ctypes.c_int

    # Simplify sloppy
    lib.meshopt_simplifySloppy.argtypes = [
        ctypes.POINTER(ctypes.c_uint),  # destination
        ctypes.POINTER(ctypes.c_uint),  # indices
        ctypes.c_size_t,                # index_count
        ctypes.POINTER(ctypes.c_float), # vertex_positions
        ctypes.c_size_t,                # vertex_count
        ctypes.c_size_t,                # vertex_positions_stride
        ctypes.POINTER(ctypes.c_ubyte), # vertex_lock
        ctypes.c_size_t,                # target_index_count
        ctypes.c_float,                 # target_error
        ctypes.POINTER(ctypes.c_float)  # result_error
    ]
    lib.meshopt_simplifySloppy.restype = ctypes.c_size_t

    # Simplify points
    lib.meshopt_simplifyPoints.argtypes = [
        ctypes.POINTER(ctypes.c_uint),  # destination
        ctypes.POINTER(ctypes.c_float), # vertex_positions
        ctypes.c_size_t,                # vertex_count
        ctypes.c_size_t,                # vertex_positions_stride
        ctypes.POINTER(ctypes.c_float), # vertex_colors
        ctypes.c_size_t,                # vertex_colors_stride
        ctypes.c_float,                 # color_weight
        ctypes.c_size_t                 # target_vertex_count
    ]
    lib.meshopt_simplifyPoints.restype = ctypes.c_size_t

    # Simplify with Attributes
    lib.meshopt_simplifyWithAttributes.argtypes = [
        ctypes.POINTER(ctypes.c_uint),  # destination
        ctypes.POINTER(ctypes.c_uint),  # indices
        ctypes.c_size_t,                # index_count
        ctypes.POINTER(ctypes.c_float), # vertex_positions
        ctypes.c_size_t,                # vertex_count
        ctypes.c_size_t,                # vertex_positions_stride
        ctypes.POINTER(ctypes.c_float), # vertex_attributes
        ctypes.c_size_t,                # vertex_attributes_stride
        ctypes.POINTER(ctypes.c_float), # attribute_weights
        ctypes.c_size_t,                # attribute_count
        ctypes.POINTER(ctypes.c_ubyte), # vertex_lock
        ctypes.c_size_t,                # target_index_count
        ctypes.c_float,                 # target_error
        ctypes.c_uint,                  # options
        ctypes.POINTER(ctypes.c_float)  # result_error
    ]
    lib.meshopt_simplifyWithAttributes.restype = ctypes.c_size_t

    # Meshlet Building
    lib.meshopt_buildMeshletsBound.argtypes = [
        ctypes.c_size_t,                # index_count
        ctypes.c_size_t,                # max_vertices
        ctypes.c_size_t                 # max_triangles
    ]
    lib.meshopt_buildMeshletsBound.restype = ctypes.c_size_t

    lib.meshopt_buildMeshlets.argtypes = [
        ctypes.c_void_p,                # meshlets
        ctypes.POINTER(ctypes.c_uint),  # meshlet_vertices
        ctypes.POINTER(ctypes.c_ubyte), # meshlet_triangles
        ctypes.POINTER(ctypes.c_uint),  # indices
        ctypes.c_size_t,                # index_count
        ctypes.POINTER(ctypes.c_float), # vertex_positions
        ctypes.c_size_t,                # vertex_count
        ctypes.c_size_t,                # vertex_positions_stride
        ctypes.c_size_t,                # max_vertices
        ctypes.c_size_t,                # max_triangles
        ctypes.c_float                  # cone_weight
    ]
    lib.meshopt_buildMeshlets.restype = ctypes.c_size_t

    lib.meshopt_buildMeshletsScan.argtypes = [
        ctypes.c_void_p,                # meshlets
        ctypes.POINTER(ctypes.c_uint),  # meshlet_vertices
        ctypes.POINTER(ctypes.c_ubyte), # meshlet_triangles
        ctypes.POINTER(ctypes.c_uint),  # indices
        ctypes.c_size_t,                # index_count
        ctypes.c_size_t,                # vertex_count
        ctypes.c_size_t,                # max_vertices
        ctypes.c_size_t                 # max_triangles
    ]
    lib.meshopt_buildMeshletsScan.restype = ctypes.c_size_t

    lib.meshopt_buildMeshletsFlex.argtypes = [
        ctypes.c_void_p,                # meshlets
        ctypes.POINTER(ctypes.c_uint),  # meshlet_vertices
        ctypes.POINTER(ctypes.c_ubyte), # meshlet_triangles
        ctypes.POINTER(ctypes.c_uint),  # indices
        ctypes.c_size_t,                # index_count
        ctypes.POINTER(ctypes.c_float), # vertex_positions
        ctypes.c_size_t,                # vertex_count
        ctypes.c_size_t,                # vertex_positions_stride
        ctypes.c_size_t,                # max_vertices
        ctypes.c_size_t,                # min_triangles
        ctypes.c_size_t,                # max_triangles
        ctypes.c_float,                 # cone_weight
        ctypes.c_float                  # split_factor
    ]
    lib.meshopt_buildMeshletsFlex.restype = ctypes.c_size_t

    lib.meshopt_buildMeshletsSpatial.argtypes = [
        ctypes.c_void_p,                # meshlets
        ctypes.POINTER(ctypes.c_uint),  # meshlet_vertices
        ctypes.POINTER(ctypes.c_ubyte), # meshlet_triangles
        ctypes.POINTER(ctypes.c_uint),  # indices
        ctypes.c_size_t,                # index_count
        ctypes.POINTER(ctypes.c_float), # vertex_positions
        ctypes.c_size_t,                # vertex_count
        ctypes.c_size_t,                # vertex_positions_stride
        ctypes.c_size_t,                # max_vertices
        ctypes.c_size_t,                # min_triangles
        ctypes.c_size_t,                # max_triangles
        ctypes.c_float                  # fill_weight
    ]
    lib.meshopt_buildMeshletsSpatial.restype = ctypes.c_size_t

    # Meshlet Optimization
    lib.meshopt_optimizeMeshlet.argtypes = [
        ctypes.POINTER(ctypes.c_uint),  # meshlet_vertices
        ctypes.POINTER(ctypes.c_ubyte), # meshlet_triangles
        ctypes.c_size_t,                # triangle_count
        ctypes.c_size_t                 # vertex_count
    ]
    lib.meshopt_optimizeMeshlet.restype = None

    lib.meshopt_optimizeMeshletLevel.argtypes = [
        ctypes.POINTER(ctypes.c_uint),  # meshlet_vertices
        ctypes.c_size_t,                # vertex_count
        ctypes.POINTER(ctypes.c_ubyte), # meshlet_triangles
        ctypes.c_size_t,                # triangle_count
        ctypes.c_int                    # level
    ]
    lib.meshopt_optimizeMeshletLevel.restype = None

    # Meshlet Bounds
    lib.meshopt_computeClusterBounds.argtypes = [
        ctypes.POINTER(ctypes.c_uint),  # indices
        ctypes.c_size_t,                # index_count
        ctypes.POINTER(ctypes.c_float), # vertex_positions
        ctypes.c_size_t,                # vertex_count
        ctypes.c_size_t                 # vertex_positions_stride
    ]
    lib.meshopt_computeClusterBounds.restype = MeshoptBounds

    lib.meshopt_computeMeshletBounds.argtypes = [
        ctypes.POINTER(ctypes.c_uint),  # meshlet_vertices
        ctypes.POINTER(ctypes.c_ubyte), # meshlet_triangles
        ctypes.c_size_t,                # triangle_count
        ctypes.POINTER(ctypes.c_float), # vertex_positions
        ctypes.c_size_t,                # vertex_count
        ctypes.c_size_t                 # vertex_positions_stride
    ]
    lib.meshopt_computeMeshletBounds.restype = MeshoptBounds

    lib.meshopt_extractMeshletIndices.argtypes = [
        ctypes.POINTER(ctypes.c_uint),  # vertices
        ctypes.POINTER(ctypes.c_ubyte), # triangles
        ctypes.POINTER(ctypes.c_uint),  # indices
        ctypes.c_size_t                 # index_count
    ]
    lib.meshopt_extractMeshletIndices.restype = ctypes.c_size_t

    # Meshlet Encoding / Decoding
    lib.meshopt_encodeMeshletBound.argtypes = [
        ctypes.c_size_t,                # max_vertices
        ctypes.c_size_t                 # max_triangles
    ]
    lib.meshopt_encodeMeshletBound.restype = ctypes.c_size_t

    lib.meshopt_encodeMeshlet.argtypes = [
        ctypes.POINTER(ctypes.c_ubyte), # buffer
        ctypes.c_size_t,                # buffer_size
        ctypes.POINTER(ctypes.c_uint),  # vertices
        ctypes.c_size_t,                # vertex_count
        ctypes.POINTER(ctypes.c_ubyte), # triangles
        ctypes.c_size_t                 # triangle_count
    ]
    lib.meshopt_encodeMeshlet.restype = ctypes.c_size_t

    lib.meshopt_decodeMeshlet.argtypes = [
        ctypes.c_void_p,                # vertices
        ctypes.c_size_t,                # vertex_count
        ctypes.c_size_t,                # vertex_size
        ctypes.c_void_p,                # triangles
        ctypes.c_size_t,                # triangle_count
        ctypes.c_size_t,                # triangle_size
        ctypes.POINTER(ctypes.c_ubyte), # buffer
        ctypes.c_size_t                 # buffer_size
    ]
    lib.meshopt_decodeMeshlet.restype = ctypes.c_int

    lib.meshopt_decodeMeshletRaw.argtypes = [
        ctypes.POINTER(ctypes.c_uint),  # vertices
        ctypes.c_size_t,                # vertex_count
        ctypes.POINTER(ctypes.c_uint),  # triangles
        ctypes.c_size_t,                # triangle_count
        ctypes.POINTER(ctypes.c_ubyte), # buffer
        ctypes.c_size_t                 # buffer_size
    ]
    lib.meshopt_decodeMeshletRaw.restype = ctypes.c_int


# Set up function signatures
try:
    setup_function_signatures()
except AttributeError as e:
    print(f"Error setting up function signatures: {e}")
    print("The library might be missing some expected functions.")
    raise
