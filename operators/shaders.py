import os
import json
from os import listdir
from os.path import join, exists, abspath, dirname
from ..const import texture_dir as tex_dir

from ..libs.blender_utils import (
  get_object, 
  get_context,
  create_collection,
  set_mode,
  add_row_with_label,
  get_data,
  get_materials,
  get_material,
  get_ops,
  active_object_,
  get_props,
  get_path,
  get_selected_object,
  get_operator,
  get_active_object,
  get_object_,
  report_warning,
  report_error
)

dir = dirname(abspath(__file__))
material_path = join(dir, '../assets/shaders/HoYoverse - Genshin Impact v3.4.blend')
outline_path = join(dir, '../assets/shaders/HoYoverse - Genshin Impact Outlines v3.blend')
post_processing_path = join(dir, '../assets/shaders/HoYoverse - Genshin Impact Post-Processing.blend')
texture_dir = None
material_dir = None
file_prefix = None

# Avatar_Girl_Sword_Furina_Mat_Face
# Avatar_Girl_Sword_Furina_Mat_Hair
# Avatar_Girl_Sword_Furina_Mat_Body
# Avatar_Girl_Sword_Furina_Mat_Dress
# Avatar_Girl_Sword_Furina_Mat_Effect
# Avatar_Default_Mat
prefix = 'HoYoverse - Genshin '
material_map = {
  'Face': f'{ prefix }Face',
  'Hair': f'{ prefix }Hair',
  'Body': f'{ prefix }Body',
  'Dress': f'{ prefix }Body',
  'Effect': f'{ prefix }Effect'
}
body_type_map = {
  'Loli': 1,
  'Boy': 2,
  'Girl': 3,
  'Male': 4,
  'Lady': 5
}

def append_node_tree (filepath, node_group_name = ''):
  with get_data().libraries.load(filepath, link = False) as (data_from, data_to):
    if node_group_name:
      data_to.node_groups.append(node_group_name)
    else:
      data_to.node_groups = data_from.node_groups

import bpy
def init_outlines (mesh_list, execute):
  def connect_node_group ():
    tree = get_context().scene.node_tree
    nodes = tree.nodes
    links = tree.links
    composite = nodes[0]
    render_layers = nodes[1]
    post_processing = nodes[2]
    links.new(render_layers.outputs[1], composite.inputs[1])
    preview = tree.nodes.new(type = 'CompositorNodeViewer')
    preview.location = (600, 300)
    links.new(render_layers.outputs[1], preview.inputs[1])
    links.new(post_processing.outputs[0], preview.inputs[0])

  def add_nodes_modifier ():
    outline_mesh = set(['Body', 'EffectHair', 'Face', 'Face_Eye'])

    for mesh in mesh_list:
      mesh_name = mesh.name

      if mesh_name in outline_mesh:
        modifier_name = 'Nodes Modifier For Outlines'
        mesh.modifiers.new(type = 'NODES', name = modifier_name)
        node_group = get_data().node_groups.get("HoYoverse - Genshin Impact Outlines")
        modifier = mesh.modifiers.get(modifier_name)
        modifier.node_group = node_group

        # 基于几何节点
        modifier["Input_12"] = True
        # 描边宽度
        modifier["Input_7"] = 0.25

        # if mesh_name == 'Body':
        modifier["Input_11"] = get_material("HoYoverse - Genshin Body")
        modifier["Input_9"] = get_material("HoYoverse - Genshin Outlines - Body")
        modifier["Input_18"] = get_material("HoYoverse - Genshin Body")
        modifier["Input_19"] = get_material("HoYoverse - Genshin Outlines - Dress")
        modifier["Input_10"] = get_material("HoYoverse - Genshin Hair")
        modifier["Input_5"] = get_material("HoYoverse - Genshin Outlines - Hair")
        # elif mesh_name == 'EffectHair':
        modifier["Input_26"] = get_material("HoYoverse - Genshin Effect")
        modifier["Input_27"] = get_material("HoYoverse - Genshin Outlines - Effect")
        # elif mesh_name == 'Face' or mesh_name == 'Face_Eye':
        modifier["Input_14"] = get_material("HoYoverse - Genshin Face")
        modifier["Input_15"] = get_material("HoYoverse - Genshin Outlines - Face")

  # TODO: delete 
  def gen_material_file_map ():
    file_names = listdir(material_dir)
    material_file_map = {}

    for file_name in file_names:
      if file_name.endswith('_Mat_Body.json'):
        material_file_map['Body'] = file_name
      elif file_name.endswith('_Mat_Dress.json'):
        material_file_map['Dress'] = file_name
      elif file_name.endswith('_Mat_Effect.json'):
        material_file_map['Effect'] = file_name
      elif file_name.endswith('_Mat_Face.json'):
        material_file_map['Face'] = file_name
      elif file_name.endswith('_Mat_Hair.json'):
        material_file_map['Hair'] = file_name

    return material_file_map

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
    node_set_image(node, f'{ type }_Diffuse.png', 'CHANNEL_PACKED')

  def init_outline_lightmap (type, material):
    node = material.node_tree.nodes['Outline_Lightmap'] 
    node_set_image(node, f'{ type }_Lightmap.png', colorspace_settings = 'Non-Color')
  
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

  # connect_node_group()
  append_node_tree(outline_path)
  material_file_map = gen_material_file_map()
  gen_outline_materials()
  init_outline_materials()
  gen_and_init_extra_outline_materials(execute)
  add_nodes_modifier()
  
def init_global_shadow (mesh_list, armature, head_bone_name):
  # 追加 head origin 和 light direction
  def append_objects ():
    active_object = get_active_object()
    collection = create_collection('Global_Shadow')
   
    with get_data().libraries.load(material_path, link = False) as (data_from, data_to):
      for name in data_from.objects:
        # Preview 会携带 Face Body Hair Outline 四种在前面已经导入过的材质
        # 如果想导入 Preview 的话，init_textures 中最开始就不用导入材质了
        if name != 'Preview':
          data_to.objects.append(name)

    for object in data_to.objects:
      collection.objects.link(object)

      if object.name != 'Light Direction':
        object.hide_set(True)

    # 如果不导入 Preview 的话，需要手动追加这个节点组
    append_node_tree(material_path, 'Light Vectors')
    active_object_(active_object)
  
  def add_nodes_modifier (mesh_list):
    for mesh in mesh_list:
      data = get_data()
      node_groups = data.node_groups
      objects = data.objects
      modifier_name = 'Nodes Modifier For Global Shadow'
      mesh.modifiers.new(type = 'NODES', name = modifier_name)
      modifier = mesh.modifiers.get(modifier_name)
      modifier.node_group = node_groups.get("Light Vectors")
      modifier["Input_3"] = objects["Light Direction"]
      modifier["Input_4"] = objects["Head Origin"]
      modifier["Input_5"] = objects["Head Forward"]
      modifier["Input_6"] = objects["Head Up"]

  def head_origin_add_child_of (armature, head_bone_name):
    head_origin = get_object_('Head Origin')
    # head origin 内部预先定义了一个
    constraint = head_origin.constraints.get('Child Of')
    constraint.target = armature
    constraint.subtarget = head_bone_name
    # TODO: 设置反向
    constraint.inverse_matrix = constraint.target.matrix_world.inverted()

  append_objects()
  append_node_tree(post_processing_path)
  add_nodes_modifier(mesh_list)
  head_origin_add_child_of(armature, head_bone_name)

def before (self, mesh_name):
  passing = None
  set_mode('OBJECT')
  mesh = get_object_(mesh_name)
  # TODO: 检查 head bone 是否存在

  if mesh:
    passing = True
    active_object_(get_object_(mesh_name))
  else:
    passing = False
    report_warning(self, f'{ mesh_name } 不存在')

  return passing

def transform_path (v):
  return os.path.abspath(get_path().abspath(v))

def import_materials ():
  # HoYoverse - Genshin Body
  # HoYoverse - Genshin Face
  # HoYoverse - Genshin Hair
  # HoYoverse - Genshin Outlines
  with get_data().libraries.load(material_path, link = False) as (data_from, data_to):
    data_to.materials = data_from.materials

def related_materials (armature):
  objects = armature.children
  # 收集 mesh，初始化全局光照时给这些 mesh 添加修改器
  mesh_list = set()

  for object in objects:
    if object.type == 'MESH':
      materials = object.data.materials

      for index, material in enumerate(materials):
        suffix = material.name.split('_')[-1]

        if suffix in material_map:
          mesh_list.add(object)
          materials[index] = get_material(material_map[suffix])

  return mesh_list

def nodes_set_image (
  nodes, 
  image_name, 
  alpha_mode = None, 
  colorspace_settings = None
):
  for node in nodes:
    node_set_image(node, image_name, alpha_mode, colorspace_settings)

def node_set_image (
  node, 
  image_name, 
  alpha_mode = None, 
  colorspace_settings = None
):
  if not image_name:
    node.image = None

    return
  
  image_name = f'{ file_prefix }_Tex_{ image_name }'
  # 先尝试从模型获取（缺少 lightmap，shadow ramp 等）
  image = get_data().images.get(image_name)

  if not image:
    image_path = join(texture_dir, image_name)

    # 3.0 之前不存在法向贴图
    if not exists(image_path):
      return
    
    image = get_data().images.load(image_path)

  if alpha_mode:
    image.alpha_mode = 'CHANNEL_PACKED'

  if colorspace_settings:
    image.colorspace_settings.name = colorspace_settings

  node.image = image

def get_nodes (material, node_name):
  nodes = material.node_tree.nodes

  # Body_Lightmap_UV0, Body_Lightmap_UV1
  return nodes[f'{ node_name }0'], nodes[f'{ node_name }1']

def init_face_diffuse (nodes):
  node_set_image(nodes['Face_Diffuse'], 'Face_Diffuse.png', 'CHANNEL_PACKED')

def init_body_type (nodes):
  # 设置脸部阴影的类型
  body_type = body_type_map[file_prefix.split('_')[1]]
  nodes["Face Shader"].inputs[0].default_value = body_type

def init_shadow_ramp (type):
  node_name = f'{ type }_Shadow_Ramp'
  node = get_data().node_groups.get(f'{ type } Shadow Ramp').nodes.get(node_name)
  node_set_image(node, f'{ node_name }.png', 'CHANNEL_PACKED')

def init_diffuse (material, type):
  node, node2 = get_nodes(material, f'{ type }_Diffuse_UV')
  image_name = f'{ type }_Diffuse.png'
  nodes_set_image([node, node2], image_name, 'CHANNEL_PACKED')

def init_lightmap (material, type):
  node, node2 = get_nodes(material, f'{ type }_Lightmap_UV')
  image_name = f'{ type }_Lightmap.png'
  nodes_set_image([node, node2], image_name, colorspace_settings = 'Non-Color')

def init_normalmap (material, type):
  node, node2 = get_nodes(material, f'{ type }_Normalmap_UV')
  image_name = f'{ type }_Normalmap.png'
  nodes_set_image([node, node2], image_name, colorspace_settings = 'Non-Color')

def reset_uv_map (material):
  # material.node_tree.nodes["UV Map"].uv_map = ""
  pass

def init_face_material ():
  nodes = get_material(f"HoYoverse - Genshin Face").node_tree.nodes
  init_face_diffuse(nodes)
  init_body_type(nodes)

def init_body_material ():
  material = get_material(f"HoYoverse - Genshin Body")
  init_shadow_ramp('Body')
  init_diffuse(material, 'Body')
  init_lightmap(material, 'Body')
  init_normalmap(material, 'Body')
  reset_uv_map(material)

def init_hair_material ():
  material = get_material(f"HoYoverse - Genshin Hair")
  init_shadow_ramp('Hair')
  init_diffuse(material, 'Hair')
  init_lightmap(material, 'Hair')
  init_normalmap(material, 'Hair')
  reset_uv_map(material)

def _init_materials ():
  init_face_material()
  init_body_material()
  init_hair_material()

def gen_and_init_effect_material(execute):
  def gen_effect_material ():
    hair_material = get_material('HoYoverse - Genshin Hair')
    effect_material = hair_material.copy()
    effect_material.name = 'HoYoverse - Genshin Effect'

    return effect_material
  
  def init_effect_material (material):
    node, node2 = get_nodes(material, 'Hair_Diffuse_UV')
    nodes_set_image([node, node2], 'EffectHair_Diffuse.png', 'CHANNEL_PACKED')
    node, node2 = get_nodes(material, 'Hair_Lightmap_UV')
    nodes_set_image([node, node2], 'EffectHair_Lightmap.png', colorspace_settings = 'Non-Color')
    node, node2 = get_nodes(material, 'Hair_Normalmap_UV')
    nodes_set_image([node, node2], None)

  if execute:
    effect_material = gen_effect_material()
    init_effect_material(effect_material)

def init_materials (armature, execute):
  import_materials()
  _init_materials()
  gen_and_init_effect_material(execute)
  mesh_list = related_materials(armature)

  return mesh_list

suffix_list = [
  'Tex_Face_Diffuse.png',
  'Tex_Body_Diffuse.png',
  'Tex_Body_Lightmap.png',
  'Tex_Body_Normalmap.png',
  'Tex_Body_Shadow_Ramp.png',
  'Tex_Hair_Diffuse.png',
  'Tex_Hair_Lightmap.png',
  'Tex_Hair_Normalmap.png',
  'Tex_Hair_Shadow_Ramp.png',
  'Tex_EffectHair_Diffuse.png',
  'Tex_EffectHair_Lightmap.png'
]

# Avatar_Girl_Sword_Furina_Tex_Body_Diffuse.png -> Body_Diffuse.png
def rename_textures ():
  images = get_data().images
    
  for image in images:
    name = image.name

    for suffix in suffix_list:
      if name.endswith(suffix):
        image.name = suffix[4:]

        break

def init_post_processing ():
  def add_node_group ():
    # 确保使用节点编辑器
    context = get_context()
    context.scene.use_nodes = True
    tree = context.scene.node_tree
    # 获取现有的节点组
    node_group_name = "HoYoverse - Post Processing"
    node_group = get_data().node_groups.get(node_group_name)
    # 添加节点组实例到合成器视图
    tree.nodes.new(type = 'CompositorNodeGroup').node_tree = node_group

  # def connect_node_group():
  #   # 确保使用节点编辑器
  #   tree = get_context().scene.node_tree
  #   nodes = tree.nodes
  #   links = tree.links

  #   composite = nodes[0]
  #   render_layers = nodes[1]
  #   post_processing = nodes[2]
  #   render_layers.location = (0, 0)
  #   composite.location = (600, 0)
  #   post_processing.location = (300, 0)
  #   links.new(render_layers.outputs[0], post_processing.inputs[0])
  #   links.new(post_processing.outputs[0], composite.inputs[0])

  def connect_node_group ():
    tree = get_context().scene.node_tree
    nodes = tree.nodes
    links = tree.links
    composite = nodes[0]
    render_layers = nodes[1]
    post_processing = nodes[2]
    # links.new(render_layers.outputs[1], composite.inputs[1])
    preview = tree.nodes.new(type = 'CompositorNodeViewer')
    preview.location = (600, 300)
    # links.new(render_layers.outputs[1], preview.inputs[1])
    # links.new(post_processing.outputs[0], preview.inputs[0])
    links.new(render_layers.outputs[0], post_processing.inputs[0])
    links.new(post_processing.outputs[0], preview.inputs[0])
    links.new(post_processing.outputs[0], composite.inputs[0])

  add_node_group()
  connect_node_group()
  # bpy.context.scene.view_settings.view_transform = 'Standard'

def run_checker (self, armature, head_bone_name, avatar):
  def check_avatar ():
    passing = True

    if avatar == 'None':
      passing = False
      report_error(self, '没有选中角色')

    return passing
  
  def check_armature ():
    passing = True

    if not armature:
      passing = False
      report_error(self, '骨架不存在')

    return passing
  
  def check_head_bone_name ():
    passing = True

    if not head_bone_name:
      passing = False
      report_error(self, '脸部阴影跟随骨骼不存在')

    return passing

  passing = True
  checkers = [
    check_avatar, 
    check_armature, 
    check_head_bone_name
  ]

  for checker in checkers:
    passing = checker()

    if not passing:
      passing = False

      break

  return passing

def init_render (self, context):
  scene = context.scene
  armature = scene.armature
  head_bone_name = scene.head_bone_name
  avatar = scene.avatar
  passing = run_checker(self, armature, head_bone_name, avatar)

  if passing:
    # rename_textures()
    global texture_dir, material_dir, file_prefix
    texture_dir = join(tex_dir, f'./{ avatar }')
    material_dir = join(texture_dir, './Materials')
    a, b, c, d, _, _ = listdir(material_dir)[0].split('_')
    file_prefix = f'{ a }_{ b }_{ c }_{ d }'
    # 按需生成 Effect 材质和描边
    execute = exists(join(material_dir, f'{ file_prefix }_Mat_Effect.json'))
    mesh_list = init_materials(armature, execute)
    init_global_shadow(mesh_list, armature, head_bone_name)
    init_outlines(mesh_list, execute)
    init_post_processing()

class OBJECT_OT_shaders (get_operator()):
  bl_idname = 'object.shaders'
  bl_label = 'Shaders'

  def execute(self, context):
    init_render(self, context)
  
    return {'FINISHED'}
