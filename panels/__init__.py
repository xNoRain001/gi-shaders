from .reload_addon import VIEW3D_PT_reload_addon
from ..libs.blender_utils import register_classes, unregister_classes, add_scene_custom_prop
from .render import VIEW3D_PT_render

classes = (
  VIEW3D_PT_reload_addon,
  VIEW3D_PT_render
)

def register():
  register_classes(classes)

def unregister():
  unregister_classes(classes)
