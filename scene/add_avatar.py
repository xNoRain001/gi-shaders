from os import listdir
from os.path import join, exists, isdir
from ..libs.blender_utils import add_scene_custom_prop, get_context
from ..utisl import get_texture_dir

name_map = {
  'Aether': '空',
  'Albedo': '阿贝多',
  'Alhatham': '艾尔海森',
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
  # 'IlCapitano': '队长',
  # 'IlDotorre': '博士',
  'Iansan': '伊安珊',
  'IlCapitano': '队长',
  'IlDotorre': '博士',
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
  'Linette': '琳妮特',
  'Lisa': '丽莎',
  'Lumine': '荧',
  'Lyney': '林尼',
  'Mavuika': '玛薇卡',
  'Mika': '米卡',
  'Mona': '莫娜',
  'Mualani': '玛拉妮',
  'Naganohara Yoimiya': '宵宫',
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
  'YaoYao': '瑶瑶',
  'Yelan': '夜兰',
  'Yun Jin': '云堇',
  'Zhongli': '钟离',
  # skin
  'Diluc - Flamme': '迪卢克 - 殷红终夜',
  'Barbara - Summer': '芭芭拉 - 闪耀协奏',
  'Fischl - Highness': '菲谢尔 - 极夜真梦',
  'Ganyu - Yu': '甘雨 - 玄玉瑶芳',
  'Jean - Summer': '琴 - 海风之梦',
  'Kaeya - Alternate': '凯亚 - 帆影游风',
  'Kamisato Ayaka - Fruhling': '绫华 - 花时来信',
  'Keqing - Feather': '刻晴 - 霓裾翩跹',
  'Kirara - Errantry': '绮良良 - 倩影游侠',
  'Klee - Alternate': '可莉 - 琪花星烛',
  'Lisa - Studentin': '丽莎 - 叶隐芳名',
  'Nilou - Fairy': '妮露 - 莎邦之息',
  'Ningguang - Floral': '凝光 - 纱中幽兰',
  'Shenhe - Dai': '申鹤 - 冷花幽露',
  'Xingqiu - Bamboo': '行秋 - 雨化竹身',
  'Furina - Funingna': '芙宁娜 - 荒' # 我猜测的
}

# 胡桃 - 宿雪桃红
# 香菱 - 岁夜欢哗

def init_items ():
  texture_dir = get_texture_dir(get_context())
  items = [("None", "None", "")]

  if not exists(texture_dir):
    return items

  dirs = listdir(texture_dir)

  # 通过材质文件生成角色列表
  for avatar in dirs:
    # 选错文件夹了
    if not isdir(join(texture_dir, avatar)):
      return
    
    if avatar == 'Baizhu':
      continue

    base = join(texture_dir, avatar)
    _dirs = listdir(base)

    # 可能存在皮肤
    if exists(join(base, 'Default')):
      if 'Materials' in _dirs:
        _dirs.remove('Materials')
      if 'Material' in _dirs:
        _dirs.remove('Material')
      if 'Censored' in _dirs:
        _dirs.remove('Censored') # 已经被和谐的模型
      # 这里文件夹命名出错了，凯亚和可莉的商城皮肤被命名成了 Alternate，
      # 只有琴、安柏、罗莎莉亚、莫娜被和谐过
      # if 'Alternate' in _dirs:
      #   _dirs.remove('Alternate') # 被和谐后修改的模型
      
      if (
        avatar == 'Jean' or # 琴
        avatar == 'Amber' or # 安柏
        avatar == 'Rosaria' or # 罗莎莉亚
        avatar == 'Mona' # 莫娜
      ):
        _dirs.remove('Alternate')
        
      # items.append((f'{ avatar }/Default', name_map[avatar], ''))
      items.append((f'{ avatar }/Default', avatar, ''))
      _dirs.remove('Default')

      if len(_dirs):
        # 此时长度为 1，因为任何角色商城只有一个皮肤
        for skin_name in _dirs:
          _avatar = f'{ avatar } - { skin_name }'

          if _avatar in name_map:
            # items.append((f'{ avatar }/{ skin_name }', name_map[_avatar], ''))
            items.append((f'{ avatar }/{ skin_name }', _avatar, ''))
          else:
            # 未翻译
            items.append((f'{ avatar }/{ skin_name }', _avatar, ''))
    else:
      # items.append((f'{ avatar }', name_map[avatar], ''))
      items.append((f'{ avatar }', avatar, ''))

  return items

def add_avatar ():
  add_scene_custom_prop(
    'avatar', 
    'Enum', 
    items = init_items(),
    # translation_context = ''
  )

  # bpy.app.timers.register(init_avatars, first_interval = 1)
