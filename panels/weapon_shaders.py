from os.path import exists
from ..libs.blender_utils import (
  get_panel, 
  get_data,
  get_ops
)

from ..operators import OBJECT_OT_weapon_shaders
from ..const import bl_category, bl_idname
from ..utisl import get_weapon_texture_dir

class VIEW3D_PT_weapon_shaders (get_panel()):
  bl_space_type = 'VIEW_3D'
  bl_region_type = 'UI'
  bl_category = bl_category
  bl_label = "Weapon Shaders"
  bl_idname = "VIEW3D_PT_Weapon_Shaders"

  def draw(self, context):
    layout = self.layout
    weapon_texture_dir = get_weapon_texture_dir(context)

    if not exists(weapon_texture_dir):
      row = layout.row()
      row.label(text = 'Go to: Edit -> Perferences -> GI Shaders -> Set weapon texture dir -> Restart blender')
      return
        
    scene = context.scene
    row = layout.row()
    row.prop(scene, 'weapon_type', text = 'Weapon type')
    row = layout.row()
    row.prop(scene, 'weapon', text = 'Weapon')
    row = layout.row()
    row.prop_search(scene, "weapon_armature", get_data(), 'objects', text = 'Armature')
    row = layout.row()
    row.operator(OBJECT_OT_weapon_shaders.bl_idname, text = 'Render')
