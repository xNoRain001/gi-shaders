from ..libs.blender_utils import add_scene_custom_prop, get_types

def add_weapon_armature ():
  add_scene_custom_prop(
    'weapon_armature', 
    'Pointer', 
    type = get_types('Object'),
    poll = lambda self, o: o.type == 'ARMATURE'
  )
