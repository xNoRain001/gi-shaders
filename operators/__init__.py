from .reload_addon import OBJECT_OT_reload_gi_shaders_addon
from .shaders import OBJECT_OT_shaders
from ..libs.blender_utils import register_classes, unregister_classes, add_scene_custom_prop

classes = (
  OBJECT_OT_reload_gi_shaders_addon,
  OBJECT_OT_shaders
)

def register():
  register_classes(classes)

def unregister():
  unregister_classes(classes)
