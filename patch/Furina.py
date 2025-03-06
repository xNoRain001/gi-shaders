from ..hooks.init_config import gen_image_path
from .utils import (
  add_outline_material, 
  add_mesh_name, 
  add_material_map, 
  add_outline_slot, 
  add_material
)

def Furina (config, image_path_prefix, json_path_prefix):
  add_mesh_name(config, 'EffectHair')
  add_material_map(config, 'Effect')
  add_outline_material(config, 'Hair', 'Effect', json_path_prefix)
  add_outline_slot(config, 'EffectHair', ['Other', 'Effect', 'Effect'])
  add_material(
    config,
    'Hair', 
    'Effect',
    gen_image_path(image_path_prefix, 'EffectHair', 'Diffuse'),
    gen_image_path(image_path_prefix, 'EffectHair', 'Lightmap'),
    ''
  )
