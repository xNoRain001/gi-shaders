from ..libs.blender_utils import register_classes, unregister_classes, add_scene_custom_prop
from .file_config import File_Config

classes = (File_Config, )

def register():
  register_classes(classes)
  add_scene_custom_prop('file_config', 'Pointer', type = File_Config)
  add_scene_custom_prop(
    'body_type', 
    'Int', 
    3, 
    'Loli / Boy / Girl / Male / Lady => [1, 5]',
    1,
    5
  )
  add_scene_custom_prop('mesh_name', 'String', default = '荧_mesh')
  add_scene_custom_prop('armature_name', 'String', default = '荧_arm')
  add_scene_custom_prop('head_bone_name', 'String', default = 'head')
  add_scene_custom_prop('light_direction_x', 'Int', default = 0)
  add_scene_custom_prop('light_direction_y', 'Int', default = 0)
  add_scene_custom_prop('light_direction_z', 'Int', default = 0)

def unregister():
  unregister_classes(classes)
