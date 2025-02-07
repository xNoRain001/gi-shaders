from ..libs.blender_utils import (
  get_props, 
  get_operator_file_list_element,
  get_operator
)

from bpy_extras.io_utils import ImportHelper

class Select_Hair_Files (get_operator(), ImportHelper):
  bl_idname = "wm.select_hair_files"
  bl_label = "Select Hair Files"
  bl_options = {'REGISTER', 'UNDO'}

  files: get_props().CollectionProperty(type=get_operator_file_list_element())
  directory: get_props().StringProperty(subtype='DIR_PATH')

  def execute(self, context):
    scene = context.scene
    mytool = scene.my_tool

    mytool.hair_files_path.clear()
    for file in self.files:
      item = mytool.hair_files_path.add()
      item.name = self.directory + file.name

    return {'FINISHED'}
