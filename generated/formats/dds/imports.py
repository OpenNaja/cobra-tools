from importlib import import_module


type_module_name_map = {
	'Byte': 'generated.formats.base.basic',
	'Ubyte': 'generated.formats.base.basic',
	'Uint64': 'generated.formats.base.basic',
	'Int64': 'generated.formats.base.basic',
	'Uint': 'generated.formats.base.basic',
	'UintHash': 'generated.formats.base.basic',
	'Ushort': 'generated.formats.base.basic',
	'Int': 'generated.formats.base.basic',
	'Short': 'generated.formats.base.basic',
	'Char': 'generated.formats.base.basic',
	'Normshort': 'generated.formats.base.basic',
	'Rangeshort': 'generated.formats.base.basic',
	'Float': 'generated.formats.base.basic',
	'Double': 'generated.formats.base.basic',
	'Hfloat': 'generated.formats.base.basic',
	'ZString': 'generated.formats.base.basic',
	'ZStringBuffer': 'generated.formats.base.compounds.ZStringBuffer',
	'ZStringBufferPadded': 'generated.formats.base.compounds.ZStringBufferPadded',
	'PadAlign': 'generated.formats.base.compounds.PadAlign',
	'FixedString': 'generated.formats.base.compounds.FixedString',
	'Vector2': 'generated.formats.base.compounds.Vector2',
	'Vector3': 'generated.formats.base.compounds.Vector3',
	'Vector3Half': 'generated.formats.base.compounds.Vector3Half',
	'Vector4': 'generated.formats.base.compounds.Vector4',
	'FourCC': 'generated.formats.dds.enums.FourCC',
	'DxgiFormat': 'generated.formats.dds.enums.DxgiFormat',
	'D3D10ResourceDimension': 'generated.formats.dds.enums.D3D10ResourceDimension',
	'HeaderFlags': 'generated.formats.dds.bitstructs.HeaderFlags',
	'PixelFormatFlags': 'generated.formats.dds.bitstructs.PixelFormatFlags',
	'Caps1': 'generated.formats.dds.bitstructs.Caps1',
	'Caps2': 'generated.formats.dds.bitstructs.Caps2',
	'PixelFormat': 'generated.formats.dds.structs.PixelFormat',
	'Dxt10Header': 'generated.formats.dds.structs.Dxt10Header',
	'Header': 'generated.formats.dds.structs.Header',
}

name_type_map = {}
for type_name, module in type_module_name_map.items():
	name_type_map[type_name] = getattr(import_module(module), type_name)
for class_object in name_type_map.values():
	if callable(getattr(class_object, 'init_attributes', None)):
		class_object.init_attributes()
