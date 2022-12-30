def create_anim(ob, anim_name):
	action = bpy.data.actions.new(name=anim_name)
	action.use_fake_user = True
	ob.animation_data_create()
	ob.animation_data.action = action
	return action