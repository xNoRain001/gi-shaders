from .init_material_config import common

def gen_json_path (json_path_prefix, body_type):
  return f'{ json_path_prefix }_Mat_{ body_type }.json'

def init_outline_material_config (json_path_prefix, global_shadow_config):
  face_material_json = gen_json_path(json_path_prefix, 'Face')
  body_material_json = gen_json_path(json_path_prefix, 'Body')
  hair_material_json = gen_json_path(json_path_prefix, 'Hair')
  dress_material_json = gen_json_path(json_path_prefix, 'Dress')
  body_diffuse = common['body_diffuse']
  body_lightmap = common['body_lightmap']
  hair_diffuse = common['hair_diffuse']
  hair_lightmap = common['hair_lightmap']

  config = {
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
    'outline_slots': {},
  }

  outline_slots = config['outline_slots']

  for mesh in global_shadow_config['mesh_list']:
    mesh_name = mesh.name

    if mesh_name.startswith('Face') and not mesh_name.startswith('Face_Eye'):
      # mesh_name slot_type material_suffix outline_material_suffix
      outline_slots[mesh_name] = [['Face', 'Face', 'Face']]
    elif mesh_name.startswith('Face_Eye'):
      outline_slots[mesh_name] = [['Face', 'Face', 'Face']]
    elif mesh_name.startswith('Body'):
      outline_slots[mesh_name] = [
        ['Body', 'Body', 'Body'],
        ['Hair', 'Hair', 'Hair'],
        ['Dress', 'Body', 'Dress']
      ]

  return config
