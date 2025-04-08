from os.path import exists
from ..libs.blender_utils import get_data, get_panel

from ..const import bl_category
from ..utisl import get_weapon_texture_dir
from ..operators import OBJECT_OT_weapon_shaders

class VIEW3D_PT_weapon_shaders (get_panel()):
  bl_region_type = 'UI'
  bl_space_type = 'VIEW_3D'
  bl_category = bl_category
  bl_label = "Weapon Shaders"
  bl_idname = "VIEW3D_PT_Weapon_Shaders"

  def draw(self, context):
    layout = self.layout
    weapon_texture_dir = get_weapon_texture_dir(context)
    box = layout.box()

    if not exists(weapon_texture_dir):
      row = box.row()
      row.label(text = 'Go to: Edit -> Perferences -> GI Shaders -> Set weapon texture dir -> Restart blender')
      return
        
    scene = context.scene
    row = box.row()
    row.prop(scene, 'weapon_type', text = 'Weapon type')
    row = box.row()
    row.prop(scene, 'weapon', text = 'Weapon')
    row = box.row()
    row.prop_search(scene, "weapon_mesh", get_data(), 'objects', text = 'Mesh')
    row = box.row()
    row.operator(OBJECT_OT_weapon_shaders.bl_idname, text = 'Render')
