from ..global_shadow_patch.utils import add_meshes

def init_global_shadow_config (armature):
  config = {
    'mesh_list': []
  }

  add_meshes(
    armature, 
    config, 
    ['Body', 'Brow', 'Face', 'Face_Eye', 'EyeStar']
  )

  return config
