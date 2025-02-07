from .reload_addon import Reload_Addon
from .render import Render
from ..libs.blender_utils import register_classes, unregister_classes, add_scene_custom_prop
from .my_property import MyProperties
from .select_body_files import Select_Body_Files
from .select_face_files import Select_Face_Files
from .select_hair_files import Select_Hair_Files

classes = (
  Reload_Addon,
  Render,
  MyProperties,
  Select_Body_Files, 
  Select_Face_Files, 
  Select_Hair_Files
)

def register():
  register_classes(classes)
  add_scene_custom_prop('my_tool', 'Pointer', type = MyProperties)

def unregister():
  unregister_classes(classes)
