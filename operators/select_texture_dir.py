from bpy_extras.io_utils import ImportHelper
from ..libs.blender_utils import get_operator, get_props, report_info

class OBJECT_OT_select_texture_dir (get_operator(), ImportHelper):
  bl_idname = "object.select_texture_dir"
  bl_label = "Select Texture  Dir"
  
  directory: get_props().StringProperty(
    name = "a",
    maxlen = 1024, # 最长为 1024 个字符
    subtype = 'DIR_PATH'
  )
  
  def execute(self, context):
    print(self.directory)
    context.scene.texture_dir = self.directory

    return {'FINISHED'}
