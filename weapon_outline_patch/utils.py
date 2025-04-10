from ..config.init_outline_material_config import gen_json_path

def add_outline_material (config, source, target, json_path_prefix, json_suffix = None):
  outline_materials = config['outline_materials']
  outline_colors = config['outline_colors']

  outline_materials[f'{ target }:Outline_Diffuse:diffuse'] = \
    outline_materials[f'{ source }:Outline_Diffuse:diffuse']
  outline_materials[f'{ target }:Outline_Lightmap:lightmap'] = \
    outline_materials[f'{ source }:Outline_Lightmap:lightmap']
  outline_colors[target] = gen_json_path(json_path_prefix, json_suffix or target)

def add_outline_colors (config, key, value, json_path_prefix):
  outline_colors = config['outline_colors']
  outline_colors[key] = gen_json_path(json_path_prefix, value)

def add_outline_slot (config, mesh_name, value):
  outline_slots = config['outline_slots']
  
  if not mesh_name in outline_slots:
    outline_slots[mesh_name] = []

  outline_slots[mesh_name].append(value)
