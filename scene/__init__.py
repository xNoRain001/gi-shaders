from ..libs.blender_utils import add_scene_custom_prop, register_classes, unregister_classes
from .add_mesh import add_mesh
from .add_avatar import add_avatar
from .add_armature import add_armature
from .add_head_origin_name import add_head_origin_name
from .add_weapon import add_weapon
from .add_weapon_mesh import add_weapon_mesh
from .add_weapon_type import add_weapon_type

# classes = ()

def register():
  # register_classes(classes)
  add_mesh()
  add_avatar()
  add_armature()
  add_head_origin_name()
  add_weapon()
  add_weapon_mesh()
  add_weapon_type()
  
def unregister():
  # unregister_classes(classes)
  pass
