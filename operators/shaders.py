from os import listdir
from os.path import join, abspath, dirname
from ..libs.blender_utils import get_operator, report_error

from ..utisl import get_texture_dir
from ..config import (
  init_material_config,
  init_global_shadow_config,
  init_outline_material_config
)
from ..hooks import (
  init_outlines, 
  init_materials, 
  init_global_shadow, 
  init_post_processing,
)
from ..material_patch import add_material_patch
from ..global_shadow_patch import add_global_shadow_patch
from ..outline_patch import add_outline_patch

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
    base = join(get_texture_dir(context), avatar)
    texture_dir = join(base, 'Textures')
    material_dir = join(base, 'Materials')
    a, b, c, d, _, _ = max(listdir(material_dir), key = len).split('_')
    file_prefix = f'{ a }_{ b }_{ c }_{ d }'
    body_type = b
    image_path_prefix = f'{ texture_dir }/{ file_prefix }'
    json_path_prefix = f'{ material_dir }/{ file_prefix }'
    material_config = init_material_config(body_type, image_path_prefix)
    _material_config = add_material_patch(material_config, avatar, image_path_prefix)
    init_materials(avatar, armature, material_path, _material_config)
    global_shadow_config = init_global_shadow_config(armature)
    _global_shadow_config = add_global_shadow_patch(armature, global_shadow_config, avatar)
    init_global_shadow(_global_shadow_config, armature, head_origin_name, material_path, avatar)
    outline_material_config = init_outline_material_config(json_path_prefix, _global_shadow_config)
    _outline_material_config = add_outline_patch(outline_material_config, avatar, json_path_prefix)
    init_outlines(_outline_material_config, outline_path, avatar)
    init_post_processing(post_processing_path)

    return {'FINISHED'}
