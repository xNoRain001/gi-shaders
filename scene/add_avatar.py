from os import listdir
from os.path import join, exists
from ..libs.blender_utils import add_scene_custom_prop
from ..const import texture_dir

def add_avatar ():
  items = [("None", "None", "")]
  dirs = listdir(texture_dir)

  # 通过材质文件生成角色列表
  for avatar in dirs:
    base = join(texture_dir, avatar)
    _dirs = listdir(base)

    # 添加其他皮肤
    if exists(join(base, 'Default')):
      items.append((f'{ avatar }/Default', avatar, ''))

      for dir in _dirs:
        if dir != 'Materials' and dir != 'Default':
          _avatar = f'{ avatar } - { dir }'
          items.append((f'{ _avatar }/{ dir }', _avatar, ''))
    else:
      items.append((f'{ avatar }', avatar, ''))

  add_scene_custom_prop(
    'avatar', 
    'Enum', 
    items = items,
    translation_context = ''
  )
