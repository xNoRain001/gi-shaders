def init_weapon_config(image_path_prefix, json_path, weapon):
  body_diffuse = image_path_prefix + '01_Tex_Diffuse.png'
  suffix = f'Weapons - { weapon }'

  return {
    'materials': {
      f'{ suffix }:Body_Diffuse_UV0': body_diffuse,
      f'{ suffix }:Body_Diffuse_UV1': body_diffuse,
    },
    'outline_materials': {
      f'{ suffix }:Outline_Diffuse:diffuse': body_diffuse
    },
    'outline_colors': {
      f'{ suffix }': json_path
    },
    'outline_slots': {
      'weapon_mesh_name': [['Other', suffix, suffix]],
    },
  }
