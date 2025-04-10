from ..const import material_prefix

def init_weapon_material_config(image_path_prefix):
  body_diffuse = image_path_prefix + '02_Tex_Diffuse.png'
  lightmap = image_path_prefix + '01_Tex_Lightmap.png'

  return {
    'materials': {
      'Weapons:Body_Diffuse_UV0:diffuse': body_diffuse,
      'Weapons:Body_Diffuse_UV1:diffuse': body_diffuse,
      'Weapons:Body_Lightmap_UV0:lightmap': lightmap,
      'Weapons:Body_Lightmap_UV1:lightmap': lightmap,
    },
    'material_map': {
      'Mat': f'{ material_prefix }Weapons',
    },
    'extra_materials': [],
  }
