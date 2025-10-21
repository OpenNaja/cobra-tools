from typing import (
    Any,
    Callable,
    Generic,
    Iterable,
    List,
    Optional,
    Tuple,
    Type,
    TypeVar,
    Union,
    overload,
)

import numpy as np
from generated.context import ContextReference

_T = TypeVar("_T")

class Array(list[_T], Generic[_T]):
    context: ContextReference
    shape: Tuple[int, ...]
    dtype: Optional[Type[_T]]
    arg: Any
    template: Any
    io_start: int
    io_size: int

    def __new__(
        cls,
        context: Any,
        arg: Any = 0,
        template: Any = None,
        shape: Union[int, Tuple[int, ...]] = (),
        dtype: Optional[Type[_T]] = None,
        set_default: bool = True,
    ) -> Union["Array[_T]", "RaggedArray[_T]", np.ndarray]: ...

    def __init__(
        self,
        context: Any,
        arg: Any = 0,
        template: Any = None,
        shape: Union[int, Tuple[int, ...]] = (),
        dtype: Optional[Type[_T]] = None,
        set_default: bool = True,
    ) -> None: ...

    @overload
    def __getitem__(self, i: int) -> _T: ...
    @overload
    def __getitem__(self, s: slice) -> List[_T]: ...

    @overload
    def __setitem__(self, i: int, o: _T) -> None: ...
    @overload
    def __setitem__(self, s: slice, o: Iterable[_T]) -> None: ...

    def set_context(self, context: Any) -> None: ...
    def set_defaults(self) -> None: ...
    def read(self, stream: Any) -> None: ...
    def write(self, stream: Any) -> None: ...
    def fill(self, function_to_generate: Callable[[], _T]) -> "Array[_T]": ...

    @classmethod
    def from_stream(
        cls,
        stream: Any,
        context: Any,
        arg: Any = 0,
        template: Any = None,
        shape: Union[int, Tuple[int, ...]] = (),
        dtype: Optional[Type[_T]] = None,
    ) -> Union["Array[_T]", "RaggedArray[_T]", np.ndarray]: ...

    @classmethod
    def to_stream(
        cls,
        instance: Any,
        stream: Any,
        context: Any,
        arg: Any = 0,
        template: Any = None,
        shape: Union[int, Tuple[int, ...]] = (),
        dtype: Optional[Type[_T]] = None,
    ) -> None: ...

    @classmethod
    def from_value(
        cls, shape: Union[int, Tuple[int, ...]], dtype: Type[_T], value: Any
    ) -> Union["Array[_T]", "RaggedArray[_T]", np.ndarray]: ...

    @property
    def ndim(self) -> int: ...
    @property
    def size(self) -> int: ...
    @property
    def class_name(self) -> str: ...

    def get_condition_fields(
        self,
        condition_function: Callable[[Any], bool],
        include_abstract: bool = True,
        enter_condition: Callable[[Any], bool] = ...,
    ) -> Iterable[Any]: ...

    @classmethod
    def get_size(
        cls,
        instance: Any,
        context: Any,
        arg: Any,
        template: Any,
        shape: Union[int, Tuple[int, ...]],
        dtype: Type[_T],
    ) -> int: ...

class RaggedArray(Array[_T]):
    @property
    def shape(self) -> Tuple[Any, ...]: ...

    def fill(self, function_to_generate: Callable[[], _T]) -> "RaggedArray[_T]": ...

    @classmethod
    def from_stream(
        cls,
        stream: Any,
        context: Any,
        arg: Any = 0,
        template: Any = None,
        shape: Union[int, Tuple[int, ...]] = (),
        dtype: Optional[Type[_T]] = None,
    ) -> Union["RaggedArray[_T]", np.ndarray]: ...
