from ..const import material_prefix

def init_weapon_material_config(image_path_prefix):
  body_diffuse = image_path_prefix + '01_Tex_Diffuse.png'

  return {
    'materials': {
      'Weapons:Body_Diffuse_UV0:diffuse': body_diffuse,
      'Weapons:Body_Diffuse_UV1:diffuse': body_diffuse,
    },
    'material_map': {
      'Mat': f'{ material_prefix }Weapons',
    },
    'extra_materials': [],
  }
