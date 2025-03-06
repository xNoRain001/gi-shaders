from ..libs.blender_utils import add_scene_custom_prop, register_classes, unregister_classes
from .add_mesh import add_mesh
from .add_avatar import add_avatar
from .add_armature import add_armature
from .add_texure_dir import add_texture_dir
from .add_head_origin_name import add_head_origin_name

# classes = ()

def register():
  # register_classes(classes)
  add_mesh()
  add_avatar()
  add_armature()
  # add_texture_dir()
  add_head_origin_name()
  
def unregister():
  # unregister_classes(classes)
  pass
