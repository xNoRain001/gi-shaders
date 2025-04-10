from os import listdir
from os.path import join, exists, abspath, dirname
from ..libs.blender_utils import get_operator, report_error

from ..utisl import get_weapon_texture_dir
from ..config import (
  init_weapon_material_config, 
  init_weapon_outline_material_config, 
)
from ..weapon_outline_patch import add_weapon_outline_patch
from ..weapon_material_patch import add_weapon_material_patch
from ..hooks import init_dissolve, init_materials, init_outlines

dir = dirname(abspath(__file__))
prefix = '../assets/shaders/HoYoverse - Genshin Impact '
outline_path = join(dir, f'{ prefix }Outlines v3.blend')
weapon_path = join(dir, f'{ prefix }Weapons - Goo Engine v3.blend')
dissolve_path = join(dir, f'{ prefix }Weapon Dissolve.blend')

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
    weapon_dir = join(get_weapon_texture_dir(context), weapon_type, weapon)
    texture_dir = join(weapon_dir, 'Textures')
    material_dir = join(weapon_dir, 'Materials')
    segments = listdir(material_dir)[0].split('_')
    file_prefix = f'{ segments[0] }_{ segments[1] }_{ segments[2] }_'
    image_path_prefix = f'{ texture_dir }/{ file_prefix }'
    json_path_prefix = f'{ material_dir }/{ file_prefix }'
    json_path = f'{ material_dir }/{ file_prefix }Mat.json'
    config = init_weapon_material_config(image_path_prefix)
    _config = add_weapon_material_patch(config, weapon, image_path_prefix)
    init_materials(weapon, weapon_mesh, weapon_path, _config, True)
    weapon_outline_material_config = init_weapon_outline_material_config(
      image_path_prefix, 
      json_path
    )
    _weapon_outline_material_config = add_weapon_outline_patch(
      weapon_outline_material_config, 
      weapon, 
      json_path_prefix
    )
    init_outlines(
      _weapon_outline_material_config, 
      outline_path, 
      weapon, 
      True, 
      weapon_mesh
    )
    init_dissolve(dissolve_path, weapon, weapon_mesh)
    
    return {'FINISHED'}
