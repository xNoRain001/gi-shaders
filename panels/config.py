from ..libs.blender_utils import get_panel, add_row_with_operator
from ..const import bl_category
from ..operators import OBJECT_OT_select_texture_dir

class VIEW3D_PT_config (get_panel()):
  bl_space_type = 'VIEW_3D'
  bl_region_type = 'UI'
  bl_category = bl_category
  bl_label = "Config"
  bl_idname = "VIEW3D_PT_config"

  def draw(self, context):
    layout = self.layout
    row = layout.row()
    row.label(text = 'Avatar Texture Dir')
    row = layout.row()
    row.operator(
      OBJECT_OT_select_texture_dir.bl_idname, 
      text = context.scene.texture_dir
    )
