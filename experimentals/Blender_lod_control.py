# TODO: save all objects of blender, operate only on scene
# save lod distance by lod name in the object to make it faster
import bpy
import re

lod_handle      = None
lod_objects     = {}
lod_collections = {}
lod_timed       = None

def getmaxlod(value):
    objs = [o for o in bpy.data.objects if o.type == 'MESH']
    maxvalue = 0
    for ob_HR in objs:
        newvalue = maxvalue
        match = re.search('lod(\d+)', ob_HR.name.lower())
        if match:
            newvalue = int(match.group(1))
        if newvalue > maxvalue and newvalue <=value:
            maxvalue = newvalue
    return maxvalue
    

def setlod(value):
    objs = [o for o in bpy.data.objects if o.type == 'MESH']
    if bpy.context.object.hiderest:
        lodstr = 'lod'+str(value)
        for ob_HR in objs:
            ob_HR.hide_render = ob_HR.hide_viewport = ob_HR.name.lower().find(lodstr.lower()) < 0
        for col in bpy.data.collections:
            col.hide_render = col.hide_viewport = col.name.lower().find(lodstr.lower()) < 0    
    else:
        for lod in range(6):
            for ob_HR in objs:
                match = re.search('lod(\d+)', ob_HR.name.lower())
                if match:
                    ob_HR.hide_render = ob_HR.hide_viewport = int(match.group(1)) > value

            for col in bpy.data.collections:
                    match = re.search('lod(\d+)', col.name.lower())
                    if match:
                        col.hide_render = col.hide_viewport = int(match.group(1)) > value


def refresh_viewport(self, context):
    """ updates viewport with current lod settings """
    maxlod = getmaxlod(bpy.context.object.lod0)
    setlod(maxlod)
    return None

def draw_callback_px(self, context):
    print("draw started")
    
    #return if no areas
    areas = [a for a in bpy.context.screen.areas if a.type == 'VIEW_3D']
    if not len(areas):
        return

    # get the first area of type VIEW_3D
    region3d = areas[0].spaces[0].region_3d

    # get the view matrix position
    view_mat_inv = region3d.view_matrix
    vwloc = view_mat_inv.to_translation()

    objs = [o for o in context.scene.objects if o.type == 'MESH']
    for ob in objs:
        print(ob.name)
        mw = ob.matrix_world
        loc1 = mw.to_translation()
        length = (vwloc - loc1).length        
        #ob.hide_render = ob.hide_viewport = length > ob.lod
        #ob.hide_viewport = True
        
        print(ob.name + " " + str(length < ob.lod))
            

    print("draw finished")


def calculate_lods(self, context):
    objs = [o for o in bpy.data.objects if o.type == 'MESH']
    lodstr = '_L' + str(0)
    for ob in objs:
        if ob.name.lower().find(lodstr.lower()) > 0:
            ob.lod  = 5
        else:
            ob.lod = 100000
    

def save_lods(self, context):
    global lod_objects
    lod_objects = []
    objs = [o for o in bpy.data.objects if o.type == 'MESH']
    for ob in objs:
        print("SAVE "  + ob.name)

def restore_lods(self, context):
    global lod_objects
    for ob in bpy.data.objects:
        print("RESTORE "  + ob.name)

def lodcontrol_toggle(self, context):
    """ enable/disable lod control and updates viewport"""
    print(bpy.context.object.lod_enable)
    global lod_handle
    global lod_timed
    if bpy.context.object.lod_enable == True:
        calculate_lods(self, context)
        save_lods(self, context)
        args = (self, context)
        bpy.app.timers.register(run_10_times)
        lod_handle = bpy.types.SpaceView3D.draw_handler_add(draw_callback_px, args, 'WINDOW', 'PRE_VIEW')
    else:
        bpy.app.timers.unregister(run_10_times)
        restore_lods(self, context)
        if lod_handle is not None:
            bpy.types.SpaceView3D.draw_handler_remove(lod_handle, 'WINDOW')
        
    print(bpy.context.object.lod_enable)
    refresh_viewport(self, context)
    return None


def run_10_times():
    print("timer started")
    
    #return if no areas
    areas = [a for a in bpy.context.screen.areas if a.type == 'VIEW_3D']
    if not len(areas):
        return

    # get the first area of type VIEW_3D
    region3d = areas[0].spaces[0].region_3d

    # get the view matrix position
    view_mat_inv = region3d.view_matrix
    vwloc = view_mat_inv.to_translation()

    objs = [o for o in bpy.context.scene.objects if o.type == 'MESH']
    for ob in objs:
        print(ob.name)
        mw = ob.matrix_world
        loc1 = mw.to_translation()
        length = (vwloc - loc1).length        
        ob.hide_render = ob.hide_viewport = length > ob.lod
        
        print(ob.name + " " + str(length < ob.lod))
            

    print("timer finished")
    return 0.1
    

class CustomDynamicPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label       = "LOD Control Panel"
    bl_idname      = "OBJECT_PT_CustomDynamicPanel"
    bl_space_type  = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category    = 'Custom Scripts'
    bl_parentid    = ''
    bl_options     = {'DEFAULT_CLOSED'}    

    def draw(self, context):
        layout = self.layout
        layout.prop(context.object,"lod_enable",text="Enable")
        layout.prop(context.object,"lod0",text="LOD0")
        layout.prop(context.object,"lod1",text="LOD1")
        layout.prop(context.object,"lod2",text="LOD2")
        layout.prop(context.object,"lod3",text="LOD3")
        layout.prop(context.object,"lod4",text="LOD4")
        layout.prop(context.object,"lod5",text="LOD5")
        layout.prop(context.object,"hiderest",text="Hide rest")
    
def register():
    bpy.types.Object._handle = None
    bpy.types.Object.lod  = bpy.props.FloatProperty( name="Dist",description="Min distance to make the object visible", min=0)

    bpy.types.Object.lod_enable = bpy.props.BoolProperty( name="Enable",description="Enables/disables lod control", update=lodcontrol_toggle )
    bpy.types.Object.lod0 = bpy.props.FloatProperty( name="Lod0",description="Desired Lod 0 distance in viewport", min=0, update=refresh_viewport )
    bpy.types.Object.lod1 = bpy.props.FloatProperty( name="Lod1",description="Desired Lod 1 distance in viewport", min=0, update=refresh_viewport )
    bpy.types.Object.lod2 = bpy.props.FloatProperty( name="Lod2",description="Desired Lod 2 distance in viewport", min=0, update=refresh_viewport )
    bpy.types.Object.lod3 = bpy.props.FloatProperty( name="Lod3",description="Desired Lod 3 distance in viewport", min=0, update=refresh_viewport )
    bpy.types.Object.lod4 = bpy.props.FloatProperty( name="Lod4",description="Desired Lod 4 distance in viewport", min=0, update=refresh_viewport )
    bpy.types.Object.lod5 = bpy.props.FloatProperty( name="Lod5",description="Desired Lod 5 distance in viewport", min=0, update=refresh_viewport )

    bpy.types.Object.hiderest = bpy.props.BoolProperty( name="All",description="Hide other lods", update=refresh_viewport )
    bpy.utils.register_class(CustomDynamicPanel)
    

def unregister():
    bpy.utils.unregister_class(CustomDynamicPanel)


if __name__ == "__main__":
    register()