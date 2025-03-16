from .reload_addon import OBJECT_OT_reload_gi_shaders_addon
from .shaders import OBJECT_OT_shaders
from .search_avatar import OBJECT_OT_Search_Avatar
from .weapon_shaders import OBJECT_OT_weapon_shaders
from ..libs.blender_utils import register_classes, unregister_classes

classes = (
  OBJECT_OT_reload_gi_shaders_addon,
  OBJECT_OT_shaders,
  OBJECT_OT_Search_Avatar,
  OBJECT_OT_weapon_shaders
)

def register():
  register_classes(classes)

def unregister():
  unregister_classes(classes)
