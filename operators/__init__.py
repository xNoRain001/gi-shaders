from .reload_addon import OBJECT_OT_reload_addon
from .render import OBJECT_OT_render
from ..libs.blender_utils import register_classes, unregister_classes, add_scene_custom_prop
from .select_body_files import OBJECT_OT_select_body_files
from .select_face_files import OBJECT_OT_select_face_files
from .select_hair_files import OBJECT_OT_select_hair_files

classes = (
  OBJECT_OT_reload_addon,
  OBJECT_OT_render,
  OBJECT_OT_select_body_files, 
  OBJECT_OT_select_face_files, 
  OBJECT_OT_select_hair_files
)

def register():
  register_classes(classes)

def unregister():
  unregister_classes(classes)
