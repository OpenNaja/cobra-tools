"""
Decoder functions for meshoptimizer.
"""
import ctypes
from typing import Union
import numpy as np
from ._loader import lib
from .limits import MeshoptLimits
from typing import Optional

def decode_vertex_buffer(vertex_count: int,
                        vertex_size: int,
                        buffer: Union[bytes, np.ndarray],
                        dtype: Optional[np.dtype] = None) -> np.ndarray:
    """
    Decode vertex buffer data.

    Args:
        vertex_count: number of vertices
        vertex_size: size of each vertex in bytes (must be multiple of 4, max 256)
        buffer: encoded buffer as bytes
        dtype: target numpy dtype for the output. If None (default), returns float32
               with automatic reshaping based on vertex_size.

    Returns:
        Numpy array containing the decoded vertex data

    Raises:
        ValueError: if parameters are invalid or would cause excessive memory allocation
        RuntimeError: if decoding fails
    """
    # Validate parameters before allocating memory
    MeshoptLimits.validate_vertex_params(vertex_count, vertex_size)

    # Convert buffer to numpy array if it's not already
    buffer_array = np.frombuffer(buffer, dtype=np.uint8)

    if dtype is not None:
        # Raw mode: decode directly to specified dtype
        destination = np.zeros(vertex_count, dtype=dtype)

        result = lib.meshopt_decodeVertexBuffer(
            destination.ctypes.data_as(ctypes.c_void_p),
            vertex_count,
            vertex_size,
            buffer_array.ctypes.data_as(ctypes.POINTER(ctypes.c_ubyte)),
            len(buffer_array)
        )

        if result != 0:
            raise RuntimeError(f"Failed to decode vertex buffer: error code {result}")

        return destination

    # Default mode: decode as float32 with automatic reshaping
    total_bytes = vertex_count * vertex_size
    destination = np.zeros(total_bytes, dtype=np.uint8)

    # Call C function
    result = lib.meshopt_decodeVertexBuffer(
        destination.ctypes.data_as(ctypes.c_void_p),
        vertex_count,
        vertex_size,
        buffer_array.ctypes.data_as(ctypes.POINTER(ctypes.c_ubyte)),
        len(buffer_array)
    )

    if result != 0:
        raise RuntimeError(f"Failed to decode vertex buffer: error code {result}")

    # Reshape the array if vertex_size indicates multiple components per vertex
    components_per_vertex = vertex_size // 4
    if components_per_vertex > 1:
        # Return as float32 with shape (vertex_count, components)
        destination = destination.view(np.float32).reshape(vertex_count, components_per_vertex)
    else:
        destination = destination.view(np.float32)

    return destination


def decode_index_buffer(index_count: int,
                       index_size: int,
                       buffer: Union[bytes, np.ndarray]) -> np.ndarray:
    """
    Decode index buffer data.

    Args:
        index_count: number of indices
        index_size: size of each index in bytes (2 or 4)
        buffer: encoded buffer as bytes

    Returns:
        Numpy array containing the decoded index data

    Raises:
        ValueError: if parameters are invalid or would cause excessive memory allocation
        RuntimeError: if decoding fails
    """
    # Validate parameters before allocating memory
    MeshoptLimits.validate_index_params(index_count, index_size)

    # Convert buffer to numpy array if it's not already
    buffer_array = np.frombuffer(buffer, dtype=np.uint8)

    # Create destination array
    destination = np.zeros(index_count, dtype=np.uint32)

    # Call C function
    result = lib.meshopt_decodeIndexBuffer(
        destination.ctypes.data_as(ctypes.c_void_p),
        index_count,
        index_size,
        buffer_array.ctypes.data_as(ctypes.POINTER(ctypes.c_ubyte)),
        len(buffer_array)
    )

    if result != 0:
        raise RuntimeError(f"Failed to decode index buffer: error code {result}")

    return destination


def decode_vertex_version(buffer: Union[bytes, np.ndarray]) -> int:
    """
    Get encoded vertex format version.

    Args:
        buffer: encoded buffer as bytes

    Returns:
        Format version of the encoded vertex buffer, or -1 if the buffer header is invalid
    """
    # Convert buffer to numpy array if it's not already
    buffer_array = np.frombuffer(buffer, dtype=np.uint8)

    return lib.meshopt_decodeVertexVersion(
        buffer_array.ctypes.data_as(ctypes.POINTER(ctypes.c_ubyte)),
        len(buffer_array)
    )


def decode_index_version(buffer: Union[bytes, np.ndarray]) -> int:
    """
    Get encoded index format version.

    Args:
        buffer: encoded buffer as bytes

    Returns:
        Format version of the encoded index buffer, or -1 if the buffer header is invalid
    """
    # Convert buffer to numpy array if it's not already
    buffer_array = np.frombuffer(buffer, dtype=np.uint8)

    return lib.meshopt_decodeIndexVersion(
        buffer_array.ctypes.data_as(ctypes.POINTER(ctypes.c_ubyte)),
        len(buffer_array)
    )


def decode_index_sequence(index_count: int,
                         index_size: int,
                         buffer: Union[bytes, np.ndarray]) -> np.ndarray:
    """
    Decode index sequence data.

    Args:
        index_count: number of indices
        index_size: size of each index in bytes (2 or 4)
        buffer: encoded buffer as bytes

    Returns:
        Numpy array containing the decoded index data

    Raises:
        ValueError: if parameters are invalid or would cause excessive memory allocation
        RuntimeError: if decoding fails
    """
    # Validate parameters before allocating memory
    MeshoptLimits.validate_index_params(index_count, index_size)

    # Convert buffer to numpy array if it's not already
    buffer_array = np.frombuffer(buffer, dtype=np.uint8)

    # Create destination array
    destination = np.zeros(index_count, dtype=np.uint32)

    # Call C function
    result = lib.meshopt_decodeIndexSequence(
        destination.ctypes.data_as(ctypes.c_void_p),
        index_count,
        index_size,
        buffer_array.ctypes.data_as(ctypes.POINTER(ctypes.c_ubyte)),
        len(buffer_array)
    )

    if result != 0:
        raise RuntimeError(f"Failed to decode index sequence: error code {result}")

    return destination


def decode_filter_oct(buffer: np.ndarray, count: int, stride: int) -> np.ndarray:
    """
    Apply octahedral filter to decoded data.

    Args:
        buffer: numpy array of decoded data
        count: number of elements
        stride: stride between elements in bytes

    Returns:
        Numpy array with the filter applied (a copy of the input buffer)
    """
    # Create a copy of the buffer to avoid modifying the original
    result_buffer = buffer.copy()

    lib.meshopt_decodeFilterOct(
        result_buffer.ctypes.data_as(ctypes.c_void_p),
        count,
        stride
    )

    return result_buffer


def decode_filter_quat(buffer: np.ndarray, count: int, stride: int) -> np.ndarray:
    """
    Apply quaternion filter to decoded data.

    Args:
        buffer: numpy array of decoded data
        count: number of elements
        stride: stride between elements in bytes

    Returns:
        Numpy array with the filter applied (a copy of the input buffer)
    """
    # Create a copy of the buffer to avoid modifying the original
    result_buffer = buffer.copy()

    lib.meshopt_decodeFilterQuat(
        result_buffer.ctypes.data_as(ctypes.c_void_p),
        count,
        stride
    )

    return result_buffer


def decode_filter_exp(buffer: np.ndarray, count: int, stride: int) -> np.ndarray:
    """
    Apply exponential filter to decoded data.

    Args:
        buffer: numpy array of decoded data
        count: number of elements
        stride: stride between elements in bytes

    Returns:
        Numpy array with the filter applied (a copy of the input buffer)
    """
    # Create a copy of the buffer to avoid modifying the original
    result_buffer = buffer.copy()

    lib.meshopt_decodeFilterExp(
        result_buffer.ctypes.data_as(ctypes.c_void_p),
        count,
        stride
    )

    return result_buffer
