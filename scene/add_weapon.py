from os import listdir
from os.path import join, exists, isdir
from ..libs.blender_utils import add_scene_custom_prop, get_context
from ..utisl import get_weapon_texture_dir, get_language

name_map = {
  # 单手剑 Sword
  # '岩峰巡歌',
  # '赦罪',
  # '有乐御簾切',
  # '静水流涌之辉',
  # '裁叶萃光',
  # '圣显之钥',
  # '波乱月白经津',
  # '雾切之回光',
  # '苍古自由之誓',
  # '磐岩结绿',
  # '斫峰之刃',
  # '风鹰剑',
  # '天空之刃'

  # 双手剑 Claymore
  # '焚曜千阳',
  # '山王长牙',
  # '裁断',
  # '苇海信标',
  # '赤角石溃杵',
  # '松籁响起之时',
  # '无工之剑',
  # '天空之傲',
  # '狼的末路'

  # 长柄武器 Polearm
  # '柔灯挽歌',
  # '赤月之形',
  # '赤沙之杖',
  # '息灾',
  # '薙草之稻光',
  # '护摩之杖',
  # '贯虹之槊',
  # '和璞鸢',
  # '天空之脊'

  # 法器 Catalyst
  # '寝正月初晴',
  # '祭星者之望',
  # '冲浪时光',
  # '鹤鸣余音',
  # '万世流涌大典',
  # '金流监督',
  # '碧落之珑',
  # '图莱杜拉的回忆',
  # '千夜浮梦',
  # '神乐之真意'  ,
  # '不灭月华',
  # '尘世之锁',
  # '四风原典',
  # '天空之卷',

  # 弓 Bow
  # '星鹫赤羽',
  # '白雨心弦',
  # '最初的大魔术',
  # '猎人之径',
  'Kirin': '若水', # Aqua Simulacra
  # '冬极白星',
  # '飞雷之弦振',
  # '终末嗟叹之诗	',
  'Amos': '阿莫斯之弓',
  # '天空之翼'
}

items = [("None", "None", "")]

def init_items ():
  old_value = 'None'

  def _init_items (self, context):
    global items
    nonlocal old_value
    weapon_type = context.scene.weapon_type

    if old_value == weapon_type:
      return items
    
    if weapon_type == 'None':
      items = [("None", "None", "")]
      old_value = weapon_type
      return items
    
    texture_dir = join(get_weapon_texture_dir(context), weapon_type)
    is_zh = get_language(get_context()) == 'ZH'
    dirs = listdir(texture_dir)

    for weapon in dirs:
      if not isdir(join(texture_dir, weapon)):
        return

      items.append((f'{ weapon }', name_map[weapon] if is_zh else weapon, ''))

    old_value = weapon_type

    return items

  return _init_items

def add_weapon ():
  add_scene_custom_prop(
    'weapon', 
    'Enum', 
    items = init_items()
  )
