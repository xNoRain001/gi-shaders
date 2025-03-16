def add_material_map (config, key, value = None):
  material_prefix = 'HoYoverse - Genshin '
  material_map = config['material_map']
  material_map[key] = material_prefix + (value or key)

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
