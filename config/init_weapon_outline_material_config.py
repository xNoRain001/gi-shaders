def init_weapon_outline_material_config(image_path_prefix, json_path):
  body_diffuse = image_path_prefix + '01_Tex_Diffuse.png'

  return {
    'outline_materials': {
      'Weapons:Outline_Diffuse:diffuse': body_diffuse
    },
    'outline_colors': {
      'Weapons': json_path
    },
    'outline_slots': {
      'weapon_mesh_name': [['Other', 'Weapons', 'Weapons']],
    },
  }
