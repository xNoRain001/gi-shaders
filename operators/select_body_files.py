from ..libs.blender_utils import (
  get_props, 
  get_operator_file_list_element,
  get_operator
)

from bpy_extras.io_utils import ImportHelper

class OBJECT_OT_select_body_files (get_operator(), ImportHelper):
  bl_idname = "object.select_body_files"
  bl_label = "Select Body Files"
  bl_options = {'REGISTER', 'UNDO'}

  files: get_props().CollectionProperty(type=get_operator_file_list_element())
  directory: get_props().StringProperty(subtype='DIR_PATH')

  def execute(self, context):
    scene = context.scene
    file_config = scene.file_config

    file_config.body_files_path.clear()
    for file in self.files:
      item = file_config.body_files_path.add()
      item.name = self.directory + file.name

    return {'FINISHED'}
 