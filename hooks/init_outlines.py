import json
from os.path import join, exists
from ..libs.blender_utils import (
  get_data,
  get_materials,
  get_material,
  append_node_tree
)

from .init_materials import node_set_image

material_dir = None
file_prefix = None
outline_path = None

def add_nodes_modifier (mesh_list):
  outline_mesh = set(['Body', 'EffectHair', 'Face', 'Face_Eye'])

  for mesh in mesh_list:
    mesh_name = mesh.name

    if mesh_name in outline_mesh:
      modifier_name = 'Nodes Modifier For Outlines'
      mesh.modifiers.new(type = 'NODES', name = modifier_name)
      node_group = get_data().node_groups.get("HoYoverse - Genshin Impact Outlines")
      modifier = mesh.modifiers.get(modifier_name)
      modifier.node_group = node_group

      modifier['Input_3_attribute_name'] = 'Col'
      # 基于几何节点
      modifier["Input_12"] = True
      # 使用顶点色
      modifier["Input_13"] = True
      # 描边宽度
      modifier["Input_7"] = 0.25

      if mesh_name == 'Body':
        modifier["Input_11"] = get_material("HoYoverse - Genshin Body")
        modifier["Input_9"] = get_material("HoYoverse - Genshin Outlines - Body")
        modifier["Input_18"] = get_material("HoYoverse - Genshin Body")
        modifier["Input_19"] = get_material("HoYoverse - Genshin Outlines - Dress")
        modifier["Input_10"] = get_material("HoYoverse - Genshin Hair")
        modifier["Input_5"] = get_material("HoYoverse - Genshin Outlines - Hair")
      elif mesh_name == 'EffectHair':
        modifier["Input_26"] = get_material("HoYoverse - Genshin Effect")
        modifier["Input_27"] = get_material("HoYoverse - Genshin Outlines - Effect")
      elif mesh_name == 'Face' or mesh_name == 'Face_Eye':
        modifier["Input_14"] = get_material("HoYoverse - Genshin Face")
        modifier["Input_15"] = get_material("HoYoverse - Genshin Outlines - Face")

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

def gen_outline_materials ():
  list = ['Body', 'Face', 'Hair']
  material_name = 'HoYoverse - Genshin Outlines'
  outline_material = get_material(material_name)

  for item in list:
    new_material = outline_material.copy()
    new_material.name = f'{ material_name } - { item }'

  # 清理材质
  get_materials().remove(outline_material)

def init_outline_diffuse (type, material):
  node = material.node_tree.nodes['Outline_Diffuse'] 
  node_set_image(node, f'{ type }_Diffuse.png', 'diffuse')

def init_outline_lightmap (type, material):
  node = material.node_tree.nodes['Outline_Lightmap'] 
  node_set_image(node, f'{ type }_Lightmap.png', 'lightmap')

def init_outline_color (type, material):
  file_path = join(material_dir, f'{ file_prefix }_Mat_{ type }.json')

  if exists(file_path):
    (
      r, g, b, a,
      r2, g2, b2, a2,
      r3, g3, b3, a3,
      r4, g4, b4, a4,
      r5, g5, b5, a5,
    ) = get_outline_color(file_path)
    outline_node = material.node_tree.nodes["Outlines"]
    outline_node.inputs[15].default_value = (r, g, b, a)
    outline_node.inputs[16].default_value = (r2, g2, b2, a2)
    outline_node.inputs[17].default_value = (r3, g3, b3, a3)
    outline_node.inputs[18].default_value = (r4, g4, b4, a4)
    outline_node.inputs[19].default_value = (r5, g5, b5, a5)

def init_body_outline_material ():
  material = get_material('HoYoverse - Genshin Outlines - Body')
  init_outline_diffuse('Body', material)
  init_outline_lightmap('Body', material)
  init_outline_color('Body', material)

def init_hair_outline_material ():
  material = get_material('HoYoverse - Genshin Outlines - Hair')
  init_outline_diffuse('Hair', material)
  init_outline_lightmap('Hair', material)
  init_outline_color('Hair', material)

def init_face_outline_material ():
  material = get_material('HoYoverse - Genshin Outlines - Face')
  init_outline_diffuse('Face', material)
  init_outline_color('Hair', material)

def init_outline_materials ():
  init_body_outline_material()
  init_hair_outline_material()
  init_face_outline_material()

def gen_and_init_extra_outline_materials (execute):
  def gen_extra_outline_materials (execute):
    # Dress Outline 不关联 Body Outline，因为描边颜色不同
    body_outline_material = get_material('HoYoverse - Genshin Outlines - Body')
    dress_outline_material = body_outline_material.copy()
    dress_outline_material.name = 'HoYoverse - Genshin Outlines - Dress'
    extral_outline_materials = [dress_outline_material]

    if execute:
      # Effect Outline 不关联 Hair Outline，因为描边颜色不同
      hair_outline_material = get_material('HoYoverse - Genshin Outlines - Hair')
      effect_outline_material = hair_outline_material.copy()
      effect_outline_material.name = 'HoYoverse - Genshin Outlines - Effect'
      extral_outline_materials.append(effect_outline_material)

    return extral_outline_materials
  
  # 只需要修改颜色
  def init_extra_outline_materials (extral_outline_materials):
    for extral_outline_material in extral_outline_materials:
      # 'HoYoverse - Genshin Outlines - Effect'
      type = extral_outline_material.name.split('-')[2][1:]
      init_outline_color(type, extral_outline_material)

  extral_outline_materials = gen_extra_outline_materials(execute)
  init_extra_outline_materials(extral_outline_materials)

def init_global_vars (_material_dir, _file_prefix, _outline_path):
  global material_dir, file_prefix, outline_path
  material_dir = _material_dir
  file_prefix = _file_prefix
  outline_path = _outline_path

def init_outlines (mesh_list, material_dir, file_prefix, outline_path, execute):
  init_global_vars(material_dir, file_prefix, outline_path)
  append_node_tree(outline_path)
  gen_outline_materials()
  init_outline_materials()
  gen_and_init_extra_outline_materials(execute)
  add_nodes_modifier(mesh_list)
  