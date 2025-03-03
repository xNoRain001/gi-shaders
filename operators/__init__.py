from .reload_addon import OBJECT_OT_reload_gi_render_addon
from .render import OBJECT_OT_render
from ..libs.blender_utils import register_classes, unregister_classes, add_scene_custom_prop

classes = (
  OBJECT_OT_reload_gi_render_addon,
  OBJECT_OT_render
)

def register():
  register_classes(classes)

def unregister():
  unregister_classes(classes)
