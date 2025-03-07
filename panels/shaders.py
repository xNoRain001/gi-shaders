from os.path import exists
from ..libs.blender_utils import (
  get_panel, 
  get_data,
  get_props,
  get_context
)

from ..operators import OBJECT_OT_shaders, OBJECT_OT_Search_Avatar
from ..const import bl_category
from ..utisl import get_texture_dir

class VIEW3D_PT_shaders (get_panel()):
  bl_space_type = 'VIEW_3D'
  bl_region_type = 'UI'
  bl_category = bl_category
  bl_label = "Shaders"
  bl_idname = "VIEW3D_PT_Shaders"

  def draw(self, context):
    layout = self.layout
    texture_dir = get_texture_dir(context)

    if not exists(texture_dir):
      row = layout.row()
      row.label(text = 'Go to: Edit -> Perferences -> GI Shaders -> Texture Dir')
      return
        
    scene = context.scene
    armature = scene.armature
    row = layout.row()
    row.prop(scene, 'avatar', text = 'Avatar')
    row = layout.row()
    # row.operator(OBJECT_OT_Search_Avatar.bl_idname, text = '', icon = 'VIEWZOOM')
    row = layout.row()
    row.prop_search(scene, "armature", get_data(), 'objects', text = 'Armature')
    
    if armature:
      row = layout.row()
      row.prop_search(scene, "head_origin_name", armature.data, 'bones', text = 'Head origin')

    row = layout.row()
    row.operator(OBJECT_OT_shaders.bl_idname, text = 'Render')
