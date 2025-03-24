from os import listdir
from os.path import join, exists, isdir
from ..libs.blender_utils import add_scene_custom_prop, get_context
from ..utisl import get_texture_dir, get_language

name_map = {
  'Aether': '空',
  'Albedo': '阿贝多',
  'Alhaitham': '艾尔海森',
  'Aloy': '埃洛伊',
  'Amber': '安柏',
  'Arataki Itto': '荒泷一斗',
  'Arlecchino': '阿蕾奇诺',
  # 'Asmoday': '阿斯莫德',
  'Asmoday': '阿斯莫德',
  'Baizhu': '白术',
  'Baizhu2': '白术2',
  'Barbara': '芭芭拉',
  'Beidou': '北斗',
  'Bennett': '班尼特',
  'Candace': '坎蒂丝',
  'Charlotte': '夏洛蒂',
  'Chasca': '恰斯卡',
  'Chevreuse': '夏沃蕾',
  'Childe': '公子',
  'Chiori': '千织',
  'Chongyun': '重云',
  'Citlali': '茜特菈莉',
  'Clorinde': '克洛琳德',
  'Collei': '柯莱',
  'Cyno': '赛诺',
  # 'Dainsleif': '戴因斯雷布',
  'Dainsleif': '戴因斯雷布',
  'Dehya': '迪希雅',
  'Diluc': '迪卢克',
  'Diona': '迪奥娜',
  'Dori': '多莉',
  'Dottore': '博士',
  # 'Dvalin': '特瓦林',
  'Dvalin': '特瓦林',
  'Emilie': '艾梅莉埃',
  'Eula': '优菈',
  'Faruzan': '珐露珊',
  'Fischl': '菲谢尔',
  'Freminet': '菲米尼',
  'Furina': '芙宁娜',
  'Gaming': '嘉明',
  'Ganyu': '甘雨',
  'Gorou': '五郎',
  'Hu Tao': '胡桃',
  # 'Iansan': '伊安珊',
  # 'Capitano': '队长',
  # 'Dotorre': '博士',
  'Iansan': '伊安珊',
  'Capitano': '队长',
  'Dotorre': '博士',
  'Jean': '琴',
  'Kachina': '卡齐娜',
  'Kaedehara Kazuha': '枫原万叶',
  'Kaeya': '凯亚',
  'Kamisato Ayaka': '神里绫华',
  'Kamisato Ayato': '神里绫人',
  'Kaveh': '卡维',
  'Keqing': '刻晴',
  'Kinich': '基尼奇',
  'Kirara': '绮良良',
  'Klee': '可莉',
  'Kujou Sara': '九条裟罗',
  'Kuki Shinobu': '久岐忍',
  # 'La Signora': '女士',
  'La Signora': '女士',
  'Layla': '莱依拉',
  'Lynette': '琳妮特',
  'Lisa': '丽莎',
  'Lumine': '荧',
  'Lyney': '林尼',
  'Mavuika': '玛薇卡',
  'Mika': '米卡',
  'Mona': '莫娜',
  'Mualani': '玛拉妮',
  'Nahida': '纳西妲',
  'Navia': '娜维娅',
  'Neuvillette': '那维莱特',
  'Nilou': '妮露',
  'Ningguang': '凝光',
  'Noelle': '诺艾尔',
  'Ororon': '欧洛伦',
  'Paimon': '派蒙',
  'Qiqi': '七七',
  'Raiden Shogun': '雷电将军',
  'Razor': '雷泽',
  'Rosaria': '罗莎莉亚',
  'Sangonomiya Kokomi': '珊瑚宫心海',
  'Sayu': '早柚',
  # 'Scaramouche': '散兵',
  'Scaramouche': '散兵',
  'Shenhe': '申鹤',
  'Shikanoin Heizou': '鹿野院平藏',
  'Sigewinne': '希格雯',
  # 'Skirk': '丝柯克',
  'Skirk': '丝柯克',
  'Sucrose': '砂糖',
  'Thoma': '托马',
  'Tighnari': '提纳里',
  'Venti': '温迪',
  'Wanderer': '流浪者',
  'Wriothesley': '莱欧斯利',
  'Xiangling': '香菱',
  'Xianyun': '闲云',
  'Xiao': '魈',
  'Xilonen': '希诺宁',
  'Xingqiu': '行秋',
  'Xinyan': '辛焱',
  'Yae Miko': '八重神子',
  'Yanfei': '烟绯',
  'Yelan': '夜兰',
  'Yun Jin': '云堇',
  'Zhongli': '钟离',
  'Focalors': '芙卡洛斯',
  'Lanyan': '蓝砚',
  'Lynette': '琳妮特',
  'Sethos': '赛索斯',
  'Signora': '赛诺',
  # 'Varesa': '瓦蕾莎',
  'Yaoyao': '瑶瑶',
  'Yoimiya': '宵宫',
  'Yumemizuki Mizuki': '梦见月瑞希',

  # 皮肤
  'Amber - 100% Outrider': '安柏 - 100%侦察骑士',
  "Jean - Gunnhildr's Legacy": '琴 - 古恩希尔德的传承',
  'Mona - Pact of Stars and Moon': '莫娜 - 星与月之约',
  "Rosaria - To the Church's Free Spirit": '罗莎莉亚 - 致教会自由人',
  "Furina - Light": '芙宁娜 - 芒',
  # 商城皮肤
  'Diluc - Red Dead of Night': '迪卢克 - 殷红终夜',
  'Barbara - Summertime Sparkle': '芭芭拉 - 闪耀协奏',
  'Fischl - Ein Immernachtstraum': '菲谢尔 - 极夜真梦',
  'Ganyu - Twilight Blossom': '甘雨 - 玄玉瑶芳',
  'Jean - Sea Breeze Dandelion': '琴 - 海风之梦',
  'Kaeya - Sailwind Shadow': '凯亚 - 帆影游风',
  'Kamisato Ayaka - Springbloom Missive': '绫华 - 花时来信',
  'Keqing - Opulent Splendor': '刻晴 - 霓裾翩跹',
  'Kirara - Phantom In Boots': '绮良良 - 倩影游侠',
  'Klee - Blossoming Starlight': '可莉 - 琪花星烛',
  'Lisa - A Sobriquet Under Shade': '丽莎 - 叶隐芳名',
  'Nilou - Breeze of Sabaa': '妮露 - 莎邦之息',
  "Ningguang - Orchid's Evening Gown": '凝光 - 纱中幽兰',
  'Shenhe - Frostflower Dew': '申鹤 - 冷花幽露',
  'Xingqiu - Bamboo Rain': '行秋 - 雨化竹身',
  'Hu Tao - Cherry Snow-Laden': '胡桃 - 宿雪桃红',
  "Xiangling - New Year's Cheer": '香菱 - 岁夜欢哗'
}

def init_items ():
  texture_dir = get_texture_dir(get_context())
  is_zh = get_language(get_context()) == 'ZH'
  items = [("None", "None", "")]

  if not exists(texture_dir):
    return items

  dirs = listdir(texture_dir)

  # 通过材质文件生成角色列表
  for avatar in dirs:
    # 选错文件夹了
    if not isdir(join(texture_dir, avatar)):
      return
    
    if avatar not in name_map:
      # print(f'{ avatar } 需要补充')
      continue

    base = join(texture_dir, avatar)
    _dirs = listdir(base)

    if len(_dirs) > 1:
      # 有皮肤
      items.append((f'{ avatar }/Default', name_map[avatar] if is_zh else avatar, ''))
      _dirs.remove('Default')

      # 删除 Default 后长度仍然可能为 2，比如琴存在商城皮肤和被和谐后的皮肤
      for skin_name in _dirs:
        _avatar = f'{ avatar } - { skin_name }'

        if _avatar in name_map:
          items.append((f'{ avatar }/{ skin_name }', name_map[_avatar] if is_zh else _avatar, ''))
        else:
          # 皮肤未翻译
          items.append((f'{ avatar }/{ skin_name }', _avatar, ''))
    else:
      items.append((f'{ avatar }/Default', name_map[avatar] if is_zh else avatar, ''))

  return items

def add_avatar ():
  add_scene_custom_prop(
    'avatar', 
    'Enum', 
    items = init_items()
  )

  # bpy.app.timers.register(init_avatars, first_interval = 1)
