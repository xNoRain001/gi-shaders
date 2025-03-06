from ..hooks.init_config import gen_json_path

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

def add_mesh_name (config, mesh_name):
  config['mesh_list'].append(mesh_name)

def add_material_map (config, key, value = None):
  material_prefix = 'HoYoverse - Genshin '
  material_map = config['material_map']
  material_map[key] = material_prefix + (value or key)

def add_outline_slot (config, mesh_name, value):
  outline_slots = config['outline_slots']
  
  if not mesh_name in outline_slots:
    outline_slots[mesh_name] = []

  outline_slots[mesh_name].append(value)

# 复制 Face 以外的材质
def add_material (config, source, target, diffuse, lightmap, normalmap):
  extra_materials = config['extra_materials']
  materials = config['materials']
  # Effect:Hair
  prefix = f'{ target }:{ source }'

  extra_materials.append(prefix)
  # shadow_ramp 是所有相关材质共有的，不需要修改
  materials[f'{ prefix }_Diffuse_UV0:diffuse'] = diffuse
  materials[f'{ prefix }_Diffuse_UV1:diffuse'] = diffuse
  materials[f'{ prefix }_Lightmap_UV0:lightmap'] = lightmap
  materials[f'{ prefix }_Lightmap_UV1:lightmap'] = lightmap
  materials[f'{ prefix }_Normalmap_UV0:normalmap'] = normalmap
  materials[f'{ prefix }_Normalmap_UV1:normalmap'] = normalmap
