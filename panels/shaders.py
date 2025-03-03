from ..libs.blender_utils import (
  get_props, 
  get_panel, 
  add_row_with_operator, 
  add_row_with_label, 
  get_operator_file_list_element,
  get_property_group,
  get_data,
  get_object_
)
from ..operators import OBJECT_OT_shaders
from ..const import bl_category

class VIEW3D_PT_shaders (get_panel()):
  bl_space_type = 'VIEW_3D'
  bl_region_type = 'UI'
  bl_category = bl_category
  bl_label = "Shaders"
  bl_idname = "VIEW3D_PT_Shaders"

  def draw(self, context):
    layout = self.layout
    scene = context.scene

    row = layout.row()
    row.prop(scene, 'avatar', text = '角色')
    row = layout.row()
    row.prop_search(scene, "armature", get_data(), 'objects', text = '骨架名称')
    
    armature = scene.armature
    if armature:
      row = layout.row()
      row.prop_search(scene, "head_bone_name", armature.data, 'bones', text = '头')

    row = layout.row()
    row.operator(OBJECT_OT_shaders.bl_idname, text = 'Render')
