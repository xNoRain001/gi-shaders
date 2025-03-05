from os import listdir
from os.path import join, exists, abspath, dirname

from ..const import texture_dir as tex_dir
from ..libs.blender_utils import get_operator, report_error, get_ops, get_context, get_data
from ..hooks import (
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

def run_checker (self, armature, head_origin_name, avatar):
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

def init_shaders (self, context):
  scene = context.scene
  avatar = scene.avatar
  armature = scene.armature
  head_origin_name = scene.head_origin_name
  passing = run_checker(self, armature, head_origin_name, avatar)

  if passing:
    # rename_textures()
    texture_dir = join(tex_dir, f'./{ avatar }')
    material_dir = join(texture_dir, './Materials')
    a, b, c, d, _, _ = listdir(material_dir)[0].split('_')
    file_prefix = f'{ a }_{ b }_{ c }_{ d }'
    # 按需生成 Effect 材质和描边
    execute = exists(join(material_dir, f'{ file_prefix }_Mat_Effect.json'))
    mesh_list = init_materials(
      armature, 
      material_path, 
      file_prefix, 
      texture_dir,
      avatar,
      execute
    )
    init_global_shadow(mesh_list, armature, head_origin_name, material_path)
    init_outlines(mesh_list, material_dir, file_prefix, outline_path, execute)
    init_post_processing(post_processing_path)

class OBJECT_OT_shaders (get_operator()):
  bl_idname = 'object.shaders'
  bl_label = 'Shaders'

  def execute(self, context):
    init_shaders(self, context)
  
    return {'FINISHED'}
