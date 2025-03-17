from os import listdir
from os.path import join, exists, isdir
from ..libs.blender_utils import add_scene_custom_prop, get_context

from ..utisl import get_language, get_weapon_texture_dir

weapon_type_map = {
  'Swords': '单手剑',
  'Claymores': '双手剑',
  'Polearms': '长柄武器',
  'Catalysts': '法器',
  'Bows': '弓'
}

def init_items ():
  items = [("None", "None", "")]
  texture_dir = get_weapon_texture_dir(get_context())
  
  if not exists(texture_dir):
    return items

  is_zh = get_language(get_context()) == 'ZH'
  dirs = listdir(texture_dir)

  for weapon_type in dirs:
    if not isdir(join(texture_dir, weapon_type)):
      return

    if weapon_type in weapon_type_map:
      items.append((
        weapon_type, 
        weapon_type_map[weapon_type] if is_zh else weapon_type, 
        ''
      ))

  return items

def add_weapon_type ():
  add_scene_custom_prop(
    'weapon_type', 
    'Enum', 
    items = init_items()
  )
