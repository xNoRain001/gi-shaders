from os.path import exists
from ..libs.blender_utils import get_data, get_panel

from ..const import bl_category
from ..utisl import get_texture_dir
from ..operators import OBJECT_OT_shaders, OBJECT_OT_Search_Avatar

class VIEW3D_PT_shaders (get_panel()):
  bl_label = "Shaders"
  bl_region_type = 'UI'
  bl_space_type = 'VIEW_3D'
  bl_category = bl_category
  bl_idname = "VIEW3D_PT_Shaders"

  def draw(self, context):
    layout = self.layout
    box = layout.box()
    texture_dir = get_texture_dir(context)
    
    if not exists(texture_dir):
      row = box.row()
      row.label(text = 'Go to: Edit -> Perferences -> GI Shaders -> Set texture dir -> Restart blender')
      return
        
    scene = context.scene
    armature = scene.armature

    row = box.row()
    row.prop(scene, 'avatar', text = 'Avatar')
    # row = box.row()
    # row.operator(OBJECT_OT_Search_Avatar.bl_idname, text = '', icon = 'VIEWZOOM')
    row = box.row()
    row.prop_search(scene, "armature", get_data(), 'objects', text = 'Armature')
    
    if armature:
      row = box.row()
      row.prop_search(
        scene, 
        "head_origin", 
        armature.data, 
        'bones', 
        text = 'Head origin'
      )

    row = box.row()
    row.operator(OBJECT_OT_shaders.bl_idname, text = 'Render')
