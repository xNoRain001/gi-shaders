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
  'Key of Khaj-Nisut': '圣显之钥',
  'Haran Geppaku Futsu': '波乱月白经津',
  'Mistsplitter Reforged': '雾切之回光',
  'Freedom-Sworn': '苍古自由之誓',
  'Primordial Jade Cutter': '磐岩结绿',
  'Summit Shaper': '斫峰之刃',
  'Aquila Favonia': '风鹰剑',
  'Skyward Blade': '天空之刃',

  # 双手剑 Claymore
  # '焚曜千阳',
  # '山王长牙',
  # '裁断',
  # '苇海信标',
  'Redhorn Stonethresher': '赤角石溃杵',
  'Song of Broken Pines': '松籁响起之时',
  'The Unforged': '无工之剑',
  'Skyward Pride': '天空之傲',
  "Wolf's Gravestone": '狼的末路',

  # 长柄武器 Polearm
  # '柔灯挽歌',
  # '赤月之形',
  'Staff of the Scarlet Sands': '赤沙之杖',
  'Calamity Queller': '息灾',
  'Engulfing Lightning': '薙草之稻光',
  'Staff of Homa': '护摩之杖',
  'Vortex Vanquisher': '贯虹之槊',
  'Primordial Jade Winged-Spear': '和璞鸢',
  'Skyward Spine': '天空之脊',

  # 法器 Catalyst
  # '寝正月初晴',
  # '祭星者之望',
  # '冲浪时光',
  # '鹤鸣余音',
  # '万世流涌大典',
  # '金流监督',
  # '碧落之珑',
  # '图莱杜拉的回忆',
  'A Thousand Floating Dreams': '千夜浮梦',
  "Kagura's Verity": '神乐之真意'  ,
  'Everlasting Moonglow': '不灭月华',
  'Memory of Dust': '尘世之锁',
  'Lost Prayer to the Sacred Winds': '四风原典',
  'Skyward Atlas': '天空之卷',

  # 弓 Bow
  # '星鹫赤羽',
  # '白雨心弦',
  # '最初的大魔术',
  "Hunter's Path": '猎人之径',
  'Aqua Simulacra': '若水',
  'Polar Star': '冬极白星',
  'Thundering Pulse': '飞雷之弦振',
  'Elegy for the End': '终末嗟叹之诗',
  "Amos' Bow": '阿莫斯之弓',
  'Skyward Harp': '天空之翼'
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
    
    items = [("None", "None", "")]
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
