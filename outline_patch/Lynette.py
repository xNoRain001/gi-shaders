from .utils import (
  add_outline_material, 
  add_outline_colors, 
  add_outline_slot
)

def Lynette (config, json_path_prefix):
  add_outline_material(config, 'Hair', 'Dress', json_path_prefix)
  add_outline_material(config, 'Body', 'Dress2', json_path_prefix)
  add_outline_colors(config, 'Dress', 'Dress1', json_path_prefix)
  add_outline_colors(config, 'Dress2', 'Dress2', json_path_prefix)
  add_outline_slot(config, 'Body', ['Dress', 'Hair', 'Dress'])
  add_outline_slot(config, 'Body', ['Dress2', 'Body', 'Dress2'])
