import os
import json

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
  get_object_
)

def append_node_tree (filepath, node_group_name = ''):
  with get_data().libraries.load(filepath, link = False) as (data_from, data_to):
    if node_group_name:
      data_to.node_groups.append(node_group_name)
    else:
      data_to.node_groups = data_from.node_groups

def init_textures (textures_dir, materials_path, body_type, materials_map):
  def add_textures (images_with_category, body_type):
    for key, value in images_with_category.items():
      type1, type2 = key.split('-')
      add_texture(type1, type2, value, textures_dir, body_type)

  def get_images_with_category (textures_dir):
    files = os.listdir(textures_dir)
    images_with_category = {
      'Face-Face_Diffuse': '',
      'Body-Body_Diffuse_UV0': '',
      'Body-Body_Lightmap_UV0': '',
      'Body-Body_Normalmap_UV0': '',
      'Body-Body_Shadow_Ramp': '',
      'Hair-Body_Diffuse_UV0': '',
      'Hair-Body_Lightmap_UV0': '',
      'Hair-Body_Normalmap_UV0': '',
      'Hair-Hair_Shadow_Ramp': ''
    }

    for file in files:
      if file.endswith('.png'):
        if file.endswith('Face_Diffuse.png'):
          images_with_category['Face-Face_Diffuse'] = file
        elif file.endswith('Body_Diffuse.png'):
          images_with_category['Body-Body_Diffuse_UV0'] = file
        elif file.endswith('Body_Lightmap.png'):
          images_with_category['Body-Body_Lightmap_UV0'] = file
        elif file.endswith('Body_Normalmap.png'):
          images_with_category['Body-Body_Normalmap_UV0'] = file
        elif file.endswith('Body_Shadow_Ramp.png'):
          images_with_category['Body-Body_Shadow_Ramp'] = file
        elif file.endswith('Hair_Diffuse.png'):
          images_with_category['Hair-Body_Diffuse_UV0'] = file
        elif file.endswith('Hair_Lightmap.png'):
          images_with_category['Hair-Body_Lightmap_UV0'] = file
        elif file.endswith('Hair_Normalmap.png'):
          images_with_category['Hair-Body_Normalmap_UV0'] = file
        elif file.endswith('Hair_Shadow_Ramp.png'):
          images_with_category['Hair-Hair_Shadow_Ramp'] = file

    return images_with_category

  def add_texture (type1, type2, value, textures_dir, body_type):
    material = get_material(f"HoYoverse - Genshin { type1 }")
    node = None

    if type2 == 'Body_Shadow_Ramp' or type2 == 'Hair_Shadow_Ramp':
      # Body_Shadow_Ramp 和 Hair_Shadow_Ramp 在节点组内设置贴图
      # Body_Shadow_Ramp => Body Shadow Ramp
      # Hair_Shadow_Ramp => Hair Shadow Ramp
      node = get_data().node_groups.get(type2.replace('_', ' ')).nodes.get(type2)
    else:
      node = material.node_tree.nodes[type2] 

    if type1 == 'Face':
      # 脸部需要设置阴影的类型
      # Loli / Boy / Girl / Male / Lady => [1, 5]
      m = get_material("HoYoverse - Genshin Face")
      m.node_tree.nodes["Face Shader"].inputs[0].default_value = body_type

    if value:
      image = get_data().images.load(os.path.join(textures_dir, value))
  
      if type2 == 'Body_Lightmap_UV0' or type2 == 'Body_Normalmap_UV0':
        # 光照贴图和法向贴图的色彩空间要设置为非色彩
        image.colorspace_settings.name = 'Non-Color'
      else:
        # 其他贴图的 Alpha 要设置为通道打包
        image.alpha_mode = 'CHANNEL_PACKED'

      node.image = image
    else:
      # 如果没有对应的贴图，就屏蔽该节点
      node.mute = True

  def related_materials (materials_map):
    materials = get_materials()

    for index, material in enumerate(materials):
      nodes = material.node_tree.nodes

      for node in nodes:
        # MMD 纹理图片
        if node.type == 'TEX_IMAGE' and node.name == 'mmd_base_tex':
          filename = os.path.basename(node.image.filepath)
          
          if filename in materials_map:
            # face | body | hair
            type = materials_map[filename]
            materials[index] = get_material(f"HoYoverse - Genshin { type.capitalize() }")
            
  def append_materials (materials_path):
    with get_data().libraries.load(materials_path, link = False) as (data_from, data_to):
      data_to.materials = data_from.materials

  append_materials(materials_path)
  images_with_category = get_images_with_category(textures_dir)
  add_textures(images_with_category, body_type)
  related_materials(materials_map)

  return images_with_category

def init_outlines (images_with_category, textures_dir, materials_dir, outlines_path, mesh_name):
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
    context = get_context()
    modifier_name = 'Nodes Modifier For Outlines'
    context.object.modifiers.new(type = 'NODES', name = modifier_name)
    node_group = get_data().node_groups.get("HoYoverse - Genshin Impact Outlines")
    modifier = context.object.modifiers.get(modifier_name)
    modifier.node_group = node_group
    get_ops().object.camera_add(align = 'VIEW')

    # TODO: 手动选择摄像机
    modifier["Input_4"] = get_object_('摄像机')
    modifier["Input_10"] = get_material("HoYoverse - Genshin Hair")
    modifier["Input_5"] = get_material("HoYoverse - Genshin Outlines - Hair")
    modifier["Input_11"] = get_material("HoYoverse - Genshin Body")
    modifier["Input_9"] = get_material("HoYoverse - Genshin Outlines - Body")
    modifier["Input_14"] = get_material("HoYoverse - Genshin Face")
    modifier["Input_15"] = get_material("HoYoverse - Genshin Outlines - Face")
    modifier["Input_12"] = True
    # 描边宽度
    modifier["Input_7"] = 1.2

  def copy_material (material_name, outline_material_name, mesh_name):
    material = get_material(material_name)
    new_material = material.copy()
    new_material.name = outline_material_name
    active_object_(get_object_(mesh_name))
    get_context().object.data.materials.append(new_material)

    return new_material

  def add_textures (images_with_category, textures_dir, materials_dir):
    material_name = 'HoYoverse - Genshin Outlines'
    material_files_with_category = get_material_files_with_category(materials_dir)

    for key, value in images_with_category.items():
      if ( 
        key.endswith('Diffuse') or
        key.endswith('Diffuse_UV0') or
        key.endswith('Lightmap_UV0') 
      ):
        type1, type2 = key.split('-')
        outline_material_name = material_name + ' - ' + type1
        outline_material = get_material(outline_material_name)

        if not outline_material:
          outline_material = copy_material(
            material_name, 
            outline_material_name, 
            mesh_name
          )

        add_texture(
          type1, 
          type2, 
          value, 
          textures_dir, 
          materials_dir, 
          material_files_with_category,
          outline_material
        )

  def get_material_files_with_category (materials_dir):
    files = os.listdir(materials_dir)
    material_files_with_category = {
      'Body': '',
      'Dress': '',
      'Face': '',
      'Hair': ''
    }

    for file in files:
      if file.endswith('Body.json'):
        material_files_with_category['Body'] = file
      elif file.endswith('Dress.json'):
        material_files_with_category['Dress'] = file
      elif file.endswith('Face.json'):
        material_files_with_category['Face'] = file
      elif file.endswith('Hair.json'):
        material_files_with_category['Hair'] = file

    return material_files_with_category

  def get_outline_color (materials_dir, material_file):
    with open(os.path.join(materials_dir, material_file), 'r', encoding = 'utf-8') as file:
      data = json.load(file)

    colors = data.get('m_SavedProperties')['m_Colors']
    outline_color = colors['_OutlineColor']
    outline_color2 = colors['_OutlineColor2']
    outline_color3 = colors['_OutlineColor3']
    outline_color4 = colors['_OutlineColor4']
    outline_color5 = colors['_OutlineColor5']
    # outline_width = saved_properties['m_Floats']['_OutlineWidth']

    return [
      outline_color['r'], outline_color['g'], outline_color['b'], outline_color['a'],
      outline_color2['r'], outline_color2['g'], outline_color2['b'], outline_color2['a'],
      outline_color3['r'], outline_color3['g'], outline_color3['b'], outline_color3['a'],
      outline_color4['r'], outline_color4['g'], outline_color4['b'], outline_color4['a'],
      outline_color5['r'], outline_color5['g'], outline_color5['b'], outline_color5['a'],
    ]

  def set_outline_color (colors, type1):
    (
      r, g, b, a,
      r2, g2, b2, a2,
      r3, g3, b3, a3,
      r4, g4, b4, a4,
      r5, g5, b5, a5,
    ) = colors
    outline_node = get_data().materials[f"HoYoverse - Genshin Outlines - { type1 }"].node_tree.nodes["Outlines"]
    outline_node.inputs[15].default_value = (r, g, b, a)
    outline_node.inputs[16].default_value = (r2, g2, b2, a2)
    outline_node.inputs[17].default_value = (r3, g3, b3, a3)
    outline_node.inputs[18].default_value = (r4, g4, b4, a4)
    outline_node.inputs[19].default_value = (r5, g5, b5, a5)

  def add_texture (
    type1, 
    type2, 
    value, 
    textures_dir, 
    materials_dir, 
    material_files_with_category,
    outline_material
  ):
    node_name = 'Outline_Diffuse' if type2.endswith('Diffuse') or type2.endswith('Diffuse_UV0') else 'Outline_Lightmap'
    node = outline_material.node_tree.nodes[node_name] 
    colors = get_outline_color(materials_dir, material_files_with_category[type1])
    set_outline_color(colors, type1)

    # bpy.data.materials["HoYoverse - Genshin Outlines - Face"].node_tree.nodes["Outlines"].inputs[6].default_value = 0
    # bpy.data.materials["HoYoverse - Genshin Outlines - Face"].node_tree.nodes["Outlines"].inputs[7].default_value = 0
    # bpy.data.materials["HoYoverse - Genshin Outlines - Face"].node_tree.nodes["Outlines"].inputs[8].default_value = 0
    # bpy.data.materials["HoYoverse - Genshin Outlines - Face"].node_tree.nodes["Outlines"].inputs[9].default_value = 0
    # bpy.data.materials["HoYoverse - Genshin Outlines - Face"].node_tree.nodes["Outlines"].inputs[10].default_value = 1

    if value:
      image = get_data().images.load(os.path.join(textures_dir, value))
  
      if type2.endswith('Lightmap_UV0'):
        image.colorspace_settings.name = 'Non-Color'
      else:
        image.alpha_mode = 'CHANNEL_PACKED'

      node.image = image
    else:
      node.mute = True

  connect_node_group()
  append_node_tree(outlines_path)
  add_textures(images_with_category, textures_dir, materials_dir)
  add_nodes_modifier()
  # TODO: 提供一个性能模式选项，用户可以选择是否删除原始的 Outline 材质

def init_global_shadow (materials_path, post_processing_path, mesh_name):
  def append_objects (materials_path, mesh_name):
    collection = create_collection('Global_Shadow')
   
    with get_data().libraries.load(materials_path, link = False) as (data_from, data_to):
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
    append_node_tree(materials_path, 'Light Vectors')
    active_object_(get_object_(mesh_name))
  
  def add_nodes_modifier ():
    context = get_context()
    data =  get_data()
    modifier_name = 'Nodes Modifier For Global Shade'
    context.object.modifiers.new(type = 'NODES', name = modifier_name)
    node_group = data.node_groups.get("Light Vectors")
    modifier = context.object.modifiers.get(modifier_name)
    modifier.node_group = node_group
    modifier["Input_3"] = data.objects["Light Direction"]
    modifier["Input_4"] = data.objects["Head Origin"]
    modifier["Input_5"] = data.objects["Head Forward"]
    modifier["Input_6"] = data.objects["Head Up"]

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

  def connect_node_group():
    # 确保使用节点编辑器
    tree = get_context().scene.node_tree
    nodes = tree.nodes
    links = tree.links

    composite = nodes[0]
    render_layers = nodes[1]
    post_processing = nodes[2]
    render_layers.location = (0, 0)
    composite.location = (600, 0)
    post_processing.location = (300, 0)
    links.new(render_layers.outputs[0], post_processing.inputs[0])
    links.new(post_processing.outputs[0], composite.inputs[0])

  def head_origin_add_child_of ():
    # TODO:
    arm_name = '荧_arm'
    head_origin = get_object('Head Origin')
    constraint = head_origin.constraints.new(type='CHILD_OF')
    arm = get_object(arm_name)
    constraint.target = arm
    active_object_(arm)
    set_mode('EDIT')
    constraint.subtarget = 'head'
    active_object_(head_origin)
    # 设置反向
    get_ops().constraint.childof_set_inverse(constraint='子级', owner='OBJECT')

  append_objects(materials_path, mesh_name)
  append_node_tree(post_processing_path)
  add_nodes_modifier()
  add_node_group()
  connect_node_group()
  # 3D视图 视图着色方式 渲染模式下 开启总是
  # bpy.context.space_data.shading.use_compositor = 'ALWAYS'
  # 关闭辉光
  # bpy.context.scene.eevee.use_bloom = False
  # head_origin_add_child_of()

def init_hair_shadow ():
  # 需要做到随光线变化 + 面部阴影融合
  material = get_material('颜')
  material.use_nodes = True
  tree = material.node_tree

  # 摄像机数据
  camera_data = tree.nodes.new(type="ShaderNodeCameraData")
  camera_data.location = (0, 0)
  # 屏幕空间信息
  screen_space_info = tree.nodes.new(type="ShaderNodeScreenspaceInfo")
  screen_space_info.location = (100, 0)
  # 合并 xyz
  combine_xyz = tree.nodes.new(type="ShaderNodeCombineXYZ")
  combine_xyz.location = (300, 0)
  # 矢量运算
  vector_math = tree.nodes.new(type="ShaderNodeVectorMath")
  vector_math.location = (400, 0)
  # 运算节点
  math = tree.nodes.new(type="ShaderNodeMath")
  math.location = (500, 0)
  math.operation = 'SUBTRACT'
  math2 = tree.nodes.new(type="ShaderNodeMath")
  math2.location = (600, 0)
  math2.operation = 'GREATER_THAN'
  math2.inputs[1].default_value = 0
  # 材质输出
  output_material = tree.nodes.new(type="ShaderNodeOutputMaterial")
  output_material.location = (700, 0)
  # 混合
  mix = tree.nodes.new(type="ShaderNodeMix")
  mix.data_type = 'RGBA'
  mix.blend_type = 'MULTIPLY'

  links = tree.links
  links.new(combine_xyz.outputs[0], vector_math.inputs[1])
  links.new(vector_math.outputs[0], screen_space_info.inputs[0])
  links.new(camera_data.outputs[0], vector_math.inputs[0])
  links.new(camera_data.outputs[1], math.inputs[0])
  links.new(screen_space_info.outputs[1], math.inputs[1])
  links.new(math.outputs[0], math2.inputs[0])
  links.new(math2.outputs[0], mix.inputs[0])
  # links.new(math2.outputs[0], mix.inputs[1])
  links.new(mix.outputs[0], output_material.inputs[0])

def init_eye_transparent ():
  return

def before ():
  set_mode('OBJECT')
  passing = True
  object = get_active_object()
  
  if object.type != 'MESH':
    passing = False

  return passing

def transform_path (v):
  return os.path.abspath(get_path().abspath(v))

def gen_materials_map (my_tool):
  types = ['face', 'body', 'hair']
  materials_map = {}

  for type in types:
    for file_path in getattr(my_tool, f'{ type }_files_path'):
      filename = os.path.basename(file_path.name)
      materials_map[filename] = type

  return materials_map

class Render (get_operator()):
  bl_idname = 'object.render'
  bl_label = 'Render'
  dir = os.path.dirname(os.path.abspath(__file__))
  post_processing_path = os.path.join(dir, '../assets/HoYoverse - Genshin Impact Post-Processing.blend')
  outlines_path = os.path.join(dir, '../assets/HoYoverse - Genshin Impact Outlines v3.blend')
  materials_path = os.path.join(dir, '../assets/HoYoverse - Genshin Impact v3.4.blend')

  def execute(self, context):
    my_tool = context.scene.my_tool
    passing = before()

    if not passing:
      self.report({'WARNING'}, "选择了错误的对象")

    materials_map = gen_materials_map(my_tool)
    # return {'FINISHED'}
    mesh_name = get_selected_object().name
    textures_dir = transform_path(my_tool.textures_dir)
    materials_dir = transform_path(my_tool.materials_dir)
    post_processing_path = self.post_processing_path
    outlines_path = self.outlines_path
    materials_path = self.materials_path
    body_type = context.scene.body_type
    images_with_category = init_textures(textures_dir, materials_path, body_type, materials_map)
    init_global_shadow(materials_path, post_processing_path, mesh_name)
    init_outlines(images_with_category, textures_dir, materials_dir, outlines_path, mesh_name)
    # TODO: 眼透 刘海阴影
    # init_hair_shadow()
    # init_eye_transparent()

    return {'FINISHED'}
