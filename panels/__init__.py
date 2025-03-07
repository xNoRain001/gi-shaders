from .reload_addon import VIEW3D_PT_reload_gi_shaders_addon
from ..libs.blender_utils import register_classes, unregister_classes, add_scene_custom_prop
from .shaders import VIEW3D_PT_shaders

classes = (
  VIEW3D_PT_reload_gi_shaders_addon,
  VIEW3D_PT_shaders
)

def register():
  register_classes(classes)

def unregister():
  unregister_classes(classes)
