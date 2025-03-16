import json
from os.path import exists
from ..libs.blender_utils import (
  get_data,
  get_materials,
  get_material,
  append_node_tree,
  get_object_
)

from .init_materials import _node_set_image
from ..const import material_prefix, outline_material_prefix

slot_map = {
  'Hair': ['Input_10', 'Input_5'],
  'Body': ['Input_11', 'Input_9'],
  'Face': ['Input_14', 'Input_15'],
  'Dress': ['Input_18', 'Input_19'],
  'Dress2': ['Input_24', 'Input_25'],
  'Other': ['Input_26', 'Input_27']
}

def update_nodes_modifier (config, is_weapon, weapon_mesh):
  outline_slots = config['outline_slots']
  modifier_name = 'Nodes Modifier For Outlines'

  for mesh_name, config in outline_slots.items():
    mesh = weapon_mesh if is_weapon else get_object_(mesh_name) 

    for item in config:
      slot_type, material_suffix, outline_material_suffix = item
      modifier = mesh.modifiers.get(modifier_name)
      slot, slot2 = slot_map[slot_type]
      modifier[slot] = get_material(material_prefix + material_suffix)
      modifier[slot2] = get_material(outline_material_prefix + outline_material_suffix)
    
def add_nodes_modifier (config, is_weapon, weapon_mesh):
  outline_slots = config['outline_slots']
  node_group = get_data().node_groups.get("HoYoverse - Genshin Impact Outlines")
  modifier_name = 'Nodes Modifier For Outlines'

  for mesh_name, config in outline_slots.items():
    mesh = weapon_mesh if is_weapon else get_object_(mesh_name) 
    mesh.modifiers.new(type = 'NODES', name = modifier_name)
    modifier = mesh.modifiers.get(modifier_name)
    modifier.node_group = node_group
    # 基于几何节点
    modifier["Input_12"] = True

    if not is_weapon:
      # 顶点色
      modifier['Input_3_attribute_name'] = 'Col'
      # 使用顶点色
      modifier["Input_13"] = True

    # 描边宽度
    modifier["Input_7"] = 0.25

def get_outline_color (file_path):
  with open(file_path, 'r', encoding = 'utf-8') as file:
    data = json.load(file)

  colors = data.get('m_SavedProperties')['m_Colors']
  
  if isinstance(colors, list):
    # 有两种形式，一种是 list，每个元素是 dict, 有 Key 和 Value 两个属性
    for item in colors:
      if item['Key'] == '_OutlineColor':
        outline_color = item['Value']
      elif item['Key'] == '_OutlineColor2':
        outline_color2 = item['Value']
      elif item['Key'] == '_OutlineColor3':
        outline_color3 = item['Value']
      elif item['Key'] == '_OutlineColor4':
        outline_color4 = item['Value']
      elif item['Key'] == '_OutlineColor5':
        outline_color5 = item['Value']
  else:
    # 另一种是 dict，直接通过属性获取值
    outline_color = colors['_OutlineColor']
    outline_color2 = colors['_OutlineColor2']
    outline_color3 = colors['_OutlineColor3']
    outline_color4 = colors['_OutlineColor4']
    outline_color5 = colors['_OutlineColor5']

  return [
    outline_color['r'], outline_color['g'], outline_color['b'], outline_color['a'],
    outline_color2['r'], outline_color2['g'], outline_color2['b'], outline_color2['a'],
    outline_color3['r'], outline_color3['g'], outline_color3['b'], outline_color3['a'],
    outline_color4['r'], outline_color4['g'], outline_color4['b'], outline_color4['a'],
    outline_color5['r'], outline_color5['g'], outline_color5['b'], outline_color5['a'],
  ]

def gen_outline_materials (config):
  outline_materials = config['outline_materials']
  outline_material = get_material('HoYoverse - Genshin Outlines')

  for key in outline_materials.keys():
    name = key.split(':')[0]
    material_name = outline_material_prefix + name

    if not get_material(material_name):
      new_material = outline_material.copy()
      new_material.name = material_name

  # 清理材质
  get_materials().remove(outline_material)

def get_node (body_type, node_name):
  nodes = get_material(outline_material_prefix + body_type).node_tree.nodes
  node = nodes[node_name]

  return node

def node_set_image (body_type, node_name, image_path, image_type):
  if not exists(image_path):
    return
  
  data = get_data()
  node = get_node(body_type, node_name)
  _node_set_image(data, node, image_path, image_type)

def init_outline_materials (config):
  outline_materials = config['outline_materials']
  for key, image_path in outline_materials.items():
    
    body_type, node_name, iamge_type = key.split(':')
    node_set_image(body_type, node_name, image_path, iamge_type)

def init_outline_color (config, is_weapon):
  outline_colors = config['outline_colors']

  for body_type, json_path in outline_colors.items():
    material = get_material(outline_material_prefix + body_type)
    (
      r, g, b, a,
      r2, g2, b2, a2,
      r3, g3, b3, a3,
      r4, g4, b4, a4,
      r5, g5, b5, a5,
    ) = get_outline_color(json_path)
    inputs = material.node_tree.nodes["Outlines"].inputs

    if is_weapon:
      inputs[17].default_value = (r, g, b, a)
      inputs[18].default_value = (r2, g2, b2, a2)
      inputs[19].default_value = (r3, g3, b3, a3)
      inputs[20].default_value = (r4, g4, b4, a4)
      inputs[21].default_value = (r5, g5, b5, a5)
    else:
      inputs[15].default_value = (r, g, b, a)
      inputs[16].default_value = (r2, g2, b2, a2)
      inputs[17].default_value = (r3, g3, b3, a3)
      inputs[18].default_value = (r4, g4, b4, a4)
      inputs[19].default_value = (r5, g5, b5, a5)

def rename_materials (avatar_or_weapon):
  materials = get_materials()

  for material in materials:
    if material.name.startswith('HoYoverse - Genshin'):
      material.name = f'{ avatar_or_weapon } - { material.name }'

def init_outlines (
  config, 
  outline_path, 
  avatar_or_weapon,
  is_weapon = False, 
  weapon_mesh = None
):
  append_node_tree(outline_path)
  gen_outline_materials(config)
  init_outline_materials(config)
  init_outline_color(config, is_weapon)
  add_nodes_modifier(config, is_weapon, weapon_mesh)
  update_nodes_modifier(config, is_weapon, weapon_mesh)
  rename_materials(avatar_or_weapon)
  