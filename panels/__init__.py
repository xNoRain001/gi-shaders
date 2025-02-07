from .reload_addon import Reload_Addon
from ..libs.blender_utils import register_classes, unregister_classes
from .render import GI_Render

classes = (
  Reload_Addon,
  GI_Render
)

def register():
  register_classes(classes)

def unregister():
  unregister_classes(classes)
