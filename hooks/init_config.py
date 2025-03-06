from ..const import material_prefix

body_type_map = {
  'Loli': 1,
  'Boy': 2,
  'Girl': 3,
  'Male': 4,
  'Lady': 5
}

def gen_image_path (image_path_prefix, body_type, image_path_suffix):
  return f'{ image_path_prefix }_Tex_{ body_type }_{ image_path_suffix }.png'

def gen_json_path (json_path_prefix, body_type):
  return f'{ json_path_prefix }_Mat_{ body_type }.json'

def init_config(avatar, image_path_prefix, json_path_prefix, file_prefix):
  face_diffuse = gen_image_path(image_path_prefix, 'Face', 'Diffuse')
  body_shadow_ramp = gen_image_path(image_path_prefix, 'Body', 'Shadow_Ramp')
  body_diffuse = gen_image_path(image_path_prefix, 'Body', 'Diffuse')
  body_lightmap = gen_image_path(image_path_prefix, 'Body', 'Lightmap')
  body_normalmap = gen_image_path(image_path_prefix, 'Body', 'Normalmap')
  hair_shadow_ramp = gen_image_path(image_path_prefix, 'Hair', 'Shadow_Ramp')
  hair_diffuse = gen_image_path(image_path_prefix, 'Hair', 'Diffuse')
  hair_lightmap = gen_image_path(image_path_prefix, 'Hair', 'Lightmap')
  hair_normalmap = gen_image_path(image_path_prefix, 'Hair', 'Normalmap')
  face_material_json = gen_json_path(json_path_prefix, 'Face')
  body_material_json = gen_json_path(json_path_prefix, 'Body')
  hair_material_json = gen_json_path(json_path_prefix, 'Hair')
  dress_material_json = gen_json_path(json_path_prefix, 'Dress')

  return {
    'body_type': body_type_map[file_prefix.split('_')[1]],
    'mesh_list': ['Face', 'Face_Eye', 'Body', 'Brow', 'EyeStar'],
    'materials': {
      'Face:Face_Diffuse:diffuse': face_diffuse,
      'Body:Body_Shadow_Ramp:shadow_ramp': body_shadow_ramp,
      'Body:Body_Diffuse_UV0:diffuse': body_diffuse,
      'Body:Body_Diffuse_UV1:diffuse': body_diffuse,
      'Body:Body_Lightmap_UV0:lightmap': body_lightmap,
      'Body:Body_Lightmap_UV1:lightmap': body_lightmap,
      'Body:Body_Normalmap_UV0:normalmap': body_normalmap,
      'Body:Body_Normalmap_UV1:normalmap': body_normalmap,
      'Hair:Hair_Shadow_Ramp:shadow_ramp': hair_shadow_ramp,
      'Hair:Hair_Diffuse_UV0:diffuse': hair_diffuse,
      'Hair:Hair_Diffuse_UV1:diffuse': hair_diffuse,
      'Hair:Hair_Lightmap_UV0:lightmap': hair_lightmap,
      'Hair:Hair_Lightmap_UV1:lightmap': hair_lightmap,
      'Hair:Hair_Normalmap_UV0:normalmap': hair_normalmap,
      'Hair:Hair_Normalmap_UV1:normalmap': hair_normalmap,
    },
    'extra_materials': [],
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
      # slot_type slot_material slot_outline_material
      'Face': [['Face', 'Face', 'Face']],
      'Face_Eye': [['Face', 'Face', 'Face']],
      'Body': [
        ['Body', 'Body', 'Body'],
        ['Hair', 'Hair', 'Hair'],
        ['Dress', 'Body', 'Dress']
      ]
    },
    'material_map': {
      'Face': f'{ material_prefix }Face',
      'Hair': f'{ material_prefix }Hair',
      'Body': f'{ material_prefix }Body',
      'Dress': f'{ material_prefix }Body'
    }
  }
