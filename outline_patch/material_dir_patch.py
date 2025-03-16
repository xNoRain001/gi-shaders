from os.path import join, exists

material_dir_map = {
  'Foo': lambda texture_dir: join(texture_dir, 'Bar'),
}

def material_dir_patch (texture_dir, material_dir, avatar):
  # Materials
  if not exists(material_dir):
    # Material
    _material_dir = material_dir[:-1]

    if exists(_material_dir):
      material_dir = _material_dir
    elif avatar in material_dir_map:
      material_dir = material_dir_map[avatar](texture_dir)

  return material_dir
