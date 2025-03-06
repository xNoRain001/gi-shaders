from .utils import (
  add_outline_material, 
  add_material_map, 
  add_outline_colors, 
  add_outline_slot
)

def Nahida (config, image_path_prefix, json_path_prefix):
  add_material_map(config, 'Dress1', 'Body')
  add_material_map(config, 'Dress2', 'Hair')
  add_outline_material(config, 'Hair', 'Dress2', json_path_prefix)
  add_outline_colors(config, 'Dress', 'Dress1', json_path_prefix)
  add_outline_colors(config, 'Dress2', 'Dress2', json_path_prefix)
  add_outline_slot(config, 'Body', ['Dress2', 'Hair', 'Dress2'])
