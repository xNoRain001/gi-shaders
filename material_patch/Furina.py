from ..config.init_material_config import gen_image_path
from .utils import (
  add_material_map, 
  add_material
)

def Furina (config, image_path_prefix):
  add_material_map(config, 'Effect')
  add_material(
    config,
    'Hair', 
    'Effect',
    gen_image_path(image_path_prefix, 'EffectHair', 'Diffuse'),
    gen_image_path(image_path_prefix, 'EffectHair', 'Lightmap'),
    ''
  )
