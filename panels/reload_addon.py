from ..libs.blender_utils import get_panel, add_row_with_operator
from ..const import bl_category

class VIEW3D_PT_reload_gi_render_addon (get_panel()):
  bl_space_type = 'VIEW_3D'
  bl_region_type = 'UI'
  bl_category = bl_category
  bl_label = "Reload GI Render Addon"
  bl_idname = "VIEW3D_PT_reload_gi_render_addon"

  def draw(self, context):
    layout = self.layout
    add_row_with_operator(layout, 'object.reload_gi_render_addon', 'Reload Addon')
