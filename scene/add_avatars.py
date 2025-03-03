from os import listdir
from ..libs.blender_utils import add_scene_custom_prop
from ..const import texture_dir

def add_avatars ():
  items = [("None", "None", "")]
  avatars = listdir(texture_dir)

  # 通过材质文件生成角色列表
  for avatar in avatars:
    items.append((avatar, avatar, ''))

  add_scene_custom_prop(
    'avatar', 
    'Enum', 
    items = items
  )
