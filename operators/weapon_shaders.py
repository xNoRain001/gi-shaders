from os import listdir
from os.path import join,  exists, abspath, dirname
from ..libs.blender_utils import get_operator, report_error

from ..utisl import get_weapon_texture_dir
from ..patch import add_patch, material_dir_patch
from ..hooks import init_weapon_config, init_weapon_materials, init_outlines

dir = dirname(abspath(__file__))
prefix = '../assets/shaders/HoYoverse - Genshin Impact '
outline_path = join(dir, f'{ prefix }Outlines v3.blend')
weapon_path = join(dir, f'{ prefix }Weapons - Goo Engine v3.blend')

def run_checker (self, context):
  def check_weapon ():
    passing = True

    if weapon == 'None':
      passing = False
      report_error(self, '没有选中武器')

    return passing
  
  def check_weapon_type ():
    passing = True

    if weapon_type == 'None':
      passing = False
      report_error(self, '武器类型不能为空')

    return passing
  
  def check_armature ():
    passing = True

    if armature == None:
      passing = False
      report_error(self, '没有选中骨架')

    return passing

  scene = context.scene
  weapon = scene.weapon
  armature = scene.weapon_armature
  weapon_type = scene.weapon_type
  passing = True
  checkers = [check_weapon_type, check_weapon, check_armature]

  for checker in checkers:
    passing = checker()

    if not passing:
      passing = False

      break

  return passing

class OBJECT_OT_weapon_shaders (get_operator()):
  bl_idname = 'object.weapon_shaders'
  bl_label = 'Weapon Shaders'

  def invoke(self, context, event):
    passing = run_checker(self, context)
  
    if passing:
      return self.execute(context)
    else:
      return {'CANCELLED'}

  def execute(self, context):
    scene = context.scene
    weapon = scene.weapon
    armature = scene.armature
    weapon_type = scene.weapon_type
    armature = scene.weapon_armature
    weapon_mesh = armature.children[0]
    texture_dir = join(get_weapon_texture_dir(context), weapon_type, weapon)
    material_dir = join(texture_dir, 'Materials')
    _material_dir = material_dir_patch(texture_dir, material_dir, weapon)
    a, b, c, _ = listdir(_material_dir)[0].split('_')
    file_prefix = f'{ a }_{ b }_{ c }_'
    image_path_prefix = f'{ texture_dir }/{ file_prefix }'
    json_path = f'{ _material_dir }/{ file_prefix }Mat.json'
    config = init_weapon_config(image_path_prefix, json_path, weapon)
    init_weapon_materials(weapon_path, config, weapon, weapon_mesh)
    # init_outlines(config, outline_path, True, weapon_mesh)
    
    return {'FINISHED'}
