from os import listdir
from os.path import join,  exists, abspath, dirname
from ..libs.blender_utils import get_operator, report_error

from ..utisl import get_weapon_texture_dir
from ..outline_patch import material_dir_patch
from ..config import (
  init_weapon_material_config, 
  init_weapon_outline_material_config, 
)
from ..hooks import init_materials, init_outlines

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
  
  def check_weapon_mesh ():
    passing = True

    if weapon_mesh == None:
      passing = False
      report_error(self, '没有选中骨架')

    return passing

  scene = context.scene
  weapon = scene.weapon
  weapon_mesh = scene.weapon_mesh
  weapon_type = scene.weapon_type
  passing = True
  checkers = [check_weapon_type, check_weapon, check_weapon_mesh]

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
    weapon_type = scene.weapon_type
    weapon_mesh = scene.weapon_mesh
    base = join(get_weapon_texture_dir(context), weapon_type, weapon)
    texture_dir = join(base, 'Textures')
    material_dir = join(base, 'Materials')
    _material_dir = material_dir_patch(texture_dir, material_dir, weapon)
    segments = listdir(_material_dir)[0].split('_')
    file_prefix = f'{ segments[0] }_{ segments[1] }_{ segments[2] }_'
    image_path_prefix = f'{ texture_dir }/{ file_prefix }'
    json_path = f'{ _material_dir }/{ file_prefix }Mat.json'
    config = init_weapon_material_config(image_path_prefix)
    init_materials(weapon_mesh, weapon_path, config, True)
    weapon_outline_material_config = init_weapon_outline_material_config(image_path_prefix, json_path)
    init_outlines(weapon_outline_material_config, outline_path, weapon, True, weapon_mesh)
    
    return {'FINISHED'}
