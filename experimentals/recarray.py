import numpy as np

from generated.formats.ovl.compounds.MemPool import MemPool
from generated.formats.ovl.compounds.RootEntry import RootEntry
from generated.formats.ovl_base import OvlContext


class Vector_record(np.record):

    def add_1(self):
        for name in self.dtype.names:
            setattr(self, name, getattr(self, name) + 1)

# demo to prove it works:
test_dtype = np.dtype((Vector_record, [("x", np.float32), ("y", np.float32), ("z", np.float32)]))
test_array = np.zeros(4, dtype=test_dtype)
print(test_array)
test_array[0].add_1()
print(test_array)

# import
c = OvlContext()
m = MemPool(c)
r = RootEntry(c)
print(m)
print(MemPool._get_np_sig(m, include_abstract=True))
print(RootEntry._get_np_sig(r, include_abstract=True))

