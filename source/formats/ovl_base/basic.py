from struct import Struct

from generated.formats.base.basic import class_from_struct


Bool = class_from_struct(Struct("<?"), bool)
