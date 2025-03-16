from os import listdir
from os.path import join, abspath, dirname
from ..libs.blender_utils import get_operator, report_error

from ..utisl import get_texture_dir
from ..patch import add_patch, material_dir_patch
from ..hooks import (
  init_config,
  init_outlines, 
  init_materials, 
  init_global_shadow, 
  init_post_processing
)

dir = dirname(abspath(__file__))
prefix = '../assets/shaders/HoYoverse - Genshin Impact '
material_path = join(dir, f'{ prefix }v3.4.blend')
outline_path = join(dir, f'{ prefix }Outlines v3.blend')
post_processing_path = join(dir, f'{ prefix }Post-Processing.blend')

def run_checker (self, context):
  def check_avatar ():
    passing = True

    if avatar == 'None':
      passing = False
      report_error(self, '没有选中角色')

    return passing
  
  def check_armature ():
    passing = True

    if not armature:
      passing = False
      report_error(self, '骨架不存在')

    return passing
  
  def check_head_origin_name ():
    passing = True

    if not head_origin_name:
      passing = False
      report_error(self, '脸部阴影跟随骨骼不存在')

    return passing
  
  scene = context.scene
  avatar = scene.avatar
  armature = scene.armature
  head_origin_name = scene.head_origin_name
  passing = True
  checkers = [
    check_avatar, 
    check_armature, 
    check_head_origin_name
  ]

  for checker in checkers:
    passing = checker()

    if not passing:
      passing = False

      break

  return passing

class OBJECT_OT_shaders (get_operator()):
  bl_idname = 'object.shaders'
  bl_label = 'Shaders'

  def invoke(self, context, event):
    passing = run_checker(self, context)
  
    if passing:
      return self.execute(context)
    else:
      return {'CANCELLED'}

  def execute(self, context):
    scene = context.scene
    avatar = scene.avatar
    armature = scene.armature
    head_origin_name = scene.head_origin_name
    texture_dir = join(get_texture_dir(context), avatar)
    material_dir = join(texture_dir, 'Materials')
    _material_dir = material_dir_patch(texture_dir, material_dir, avatar)
    a, b, c, d, _, _ = listdir(_material_dir)[0].split('_')
    file_prefix = f'{ a }_{ b }_{ c }_{ d }'
    image_path_prefix = f'{ texture_dir }/{ file_prefix }'
    json_path_prefix = f'{ _material_dir }/{ file_prefix }'
    config = init_config(avatar, image_path_prefix, json_path_prefix, file_prefix)
    _config = add_patch(config, avatar, image_path_prefix, json_path_prefix)
    init_materials(armature, material_path, _config)
    init_global_shadow(_config, armature, head_origin_name, material_path)
    init_outlines(_config, outline_path)
    init_post_processing(post_processing_path)
  
    return {'FINISHED'}
