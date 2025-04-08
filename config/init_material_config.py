from ..const import material_prefix

body_type_map = {
  'Loli': 1,
  'Boy': 2,
  'Girl': 3,
  'Male': 4,
  'Lady': 5
}
common = {
  'body_diffuse': None,
  'body_lightmap': None,
  'hair_diffuse': None,
  'hair_lightmap': None
}

def gen_image_path (image_path_prefix, body_type, image_path_suffix):
  return f'{ image_path_prefix }_Tex_{ body_type }_{ image_path_suffix }.png'

def init_material_config (body_type, image_path_prefix):
  face_diffuse = gen_image_path(image_path_prefix, 'Face', 'Diffuse')
  body_shadow_ramp = gen_image_path(image_path_prefix, 'Body', 'Shadow_Ramp')
  common['body_diffuse'] = body_diffuse = gen_image_path(image_path_prefix, 'Body', 'Diffuse')
  common['body_lightmap'] = body_lightmap = gen_image_path(image_path_prefix, 'Body', 'Lightmap')
  body_normalmap = gen_image_path(image_path_prefix, 'Body', 'Normalmap')
  hair_shadow_ramp = gen_image_path(image_path_prefix, 'Hair', 'Shadow_Ramp')
  common['hair_diffuse'] = hair_diffuse = gen_image_path(image_path_prefix, 'Hair', 'Diffuse')
  common['hair_lightmap'] = hair_lightmap = gen_image_path(image_path_prefix, 'Hair', 'Lightmap')
  hair_normalmap = gen_image_path(image_path_prefix, 'Hair', 'Normalmap')
  config = {
    'body_type': body_type_map[body_type],
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
    'material_map': {
      # 默认材质的后缀 新材质的名称
      'Face': f'{ material_prefix }Face',
      'Hair': f'{ material_prefix }Hair',
      'Body': f'{ material_prefix }Body',
      'Dress': f'{ material_prefix }Body'
    }
  }

  return config
