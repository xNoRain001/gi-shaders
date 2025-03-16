from .init_material_config import common

def gen_json_path (json_path_prefix, body_type):
  return f'{ json_path_prefix }_Mat_{ body_type }.json'

def init_outline_material_config (avatar, json_path_prefix):
  face_material_json = gen_json_path(json_path_prefix, 'Face')
  body_material_json = gen_json_path(json_path_prefix, 'Body')
  hair_material_json = gen_json_path(json_path_prefix, 'Hair')
  dress_material_json = gen_json_path(json_path_prefix, 'Dress')
  body_diffuse = common['body_diffuse']
  body_lightmap = common['body_lightmap']
  hair_diffuse = common['hair_diffuse']
  hair_lightmap = common['hair_lightmap']

  return {
    'outline_materials': {
      'Face:Outline_Diffuse:diffuse': '',
      'Face:Outline_Lightmap:lightmap': '',
      'Body:Outline_Diffuse:diffuse': body_diffuse,
      'Body:Outline_Lightmap:lightmap': body_lightmap,
      'Dress:Outline_Diffuse:diffuse': body_diffuse,
      'Dress:Outline_Lightmap:lightmap': body_lightmap,
      'Hair:Outline_Diffuse:diffuse': hair_diffuse,
      'Hair:Outline_Lightmap:lightmap': hair_lightmap,
    },
    'outline_colors': {
      'Face': face_material_json,
      'Body': body_material_json,
      'Hair': hair_material_json,
      'Dress': dress_material_json
    },
    'outline_slots': {
      # mesh_name slot_type material_suffix outline_material_suffix
      'Face': [['Face', 'Face', 'Face']],
      'Face_Eye': [['Face', 'Face', 'Face']],
      'Body': [
        ['Body', 'Body', 'Body'],
        ['Hair', 'Hair', 'Hair'],
        ['Dress', 'Body', 'Dress']
      ]
    },
  }
