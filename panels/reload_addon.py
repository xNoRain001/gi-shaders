from ..libs.blender_utils import get_panel, add_row_with_operator

class Reload_Addon(get_panel()):
  bl_space_type = 'VIEW_3D'
  bl_region_type = 'UI'
  bl_category = 'Item'
  bl_label = "Reload Addon"
  bl_idname = "_PT_Reload_Addon_PT_"

  def draw(self, context):
    layout = self.layout
    add_row_with_operator(layout, 'object.reload_addon', 'Reload Addon')
