import bpy
from collections import defaultdict

# adapted from
# https://blender.stackexchange.com/questions/157828/how-to-duplicate-a-certain-collection-using-python


def copy_objects(from_col, to_col, linked, dupe_lut, replacer):
	for o in from_col.objects:
		dupe = o.copy()
		dupe.name = replacer(o.name)
		if not linked and o.data:
			dupe.data = dupe.data.copy()
			dupe.data.name = replacer(dupe.data.name)
		to_col.objects.link(dupe)
		dupe_lut[o] = dupe


def copy(parent, collection, linked=False, replacer=None):
	assert parent != collection
	dupe_lut = defaultdict(lambda: None)

	def _copy(parent, collection, linked=False):
		cc = bpy.data.collections.new(replacer(collection.name))
		copy_objects(collection, cc, linked, dupe_lut, replacer)

		for c in collection.children:
			_copy(cc, c, linked)

		parent.children.link(cc)

	_copy(parent, collection, linked)
	# print(dupe_lut)
	for o, dupe in tuple(dupe_lut.items()):
		parent = dupe_lut[o.parent]
		if parent:
			dupe.parent = parent
