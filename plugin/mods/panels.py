from plugin.utils.panels import PropertiesPanel


class COBRA_MOD_PT_mod(PropertiesPanel):
	"""Creates a Panel in the Collection properties window for mod attributes"""
	bl_label = "Cobra Mod information"
	bl_context = "collection"

	def draw(self, context):
		mod = context.collection.mod
		self.layout.prop(mod, "name")
		self.layout.prop(mod, "desc")
		self.layout.prop(mod, "game")
		self.layout.prop(mod, "uuid")
		if mod.game == 'JURASSIC_WORLD_EVOLUTION_2':
			self.layout.prop(mod, "ordid")
		self.layout.prop(mod, "path")
		# todo - re-add operators
		# self.layout.operator("cobra.export_mod")
		self.layout.prop(mod, "pack")
		# self.layout.operator("cobra.pack_mod")


class COBRA_MOD_PT_scenery(PropertiesPanel):
	"""Creates a Panel in the Object properties window for Scenery asset attributes"""
	bl_label = "Cobra Asset information"
	bl_context = "object"

	def draw(self, context):
		scenery = context.object.scenery
		self.layout.prop(scenery, "name")
		self.layout.prop(scenery, "desc")

		row = self.layout.row()
		row.label(text="Gameplay", icon='WORLD_DATA')
		row.prop(scenery, "price")
		row.prop(scenery, "cost")

		# todo - re-add operator
		# self.layout.operator("cobra.generate_icon")
