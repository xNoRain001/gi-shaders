from ..libs.blender_utils import (
  create_collection,
  get_data,
  active_object_,
  get_active_object,
  get_object_,
  append_node_tree,
  get_ops,
  active_object_
)

material_path = None

# 追加 head origin 和 light direction
def append_objects (avatar):
  active_object = get_active_object()
  collection = create_collection(f'Global_Shadow_{ avatar }')
  
  with get_data().libraries.load(material_path, link = False) as (data_from, data_to):
    for name in data_from.objects:
      # Preview 会携带 Face Body Hair Outline 四种在前面已经导入过的材质
      # 如果想导入 Preview 的话，init_textures 中最开始就不用导入材质了
      if name != 'Preview':
        data_to.objects.append(name)

  for object in data_to.objects:
    object.name = object.name + '_' + avatar
    collection.objects.link(object)

    if object.name != f'Light Direction_{ avatar }':
      object.hide_set(True)

  # 如果不导入 Preview 的话，需要手动追加这个节点组
  node_name = 'Light Vectors'
  append_node_tree(material_path, node_name, f'{ node_name }_{ avatar }')
  active_object_(active_object)

def add_nodes_modifier (config, avatar):
  def _add_modifier (mesh, node_groups, objects):
    modifier_name = 'Nodes Modifier For Global Shadow'
    modifier = mesh.modifiers.new(type = 'NODES', name = modifier_name)
    modifier.node_group = node_groups.get(f"Light Vectors_{ avatar }")
    modifier["Input_3"] = objects[f"Light Direction_{ avatar }"]
    modifier["Input_4"] = objects[f"Head Origin_{ avatar }"]
    modifier["Input_5"] = objects[f"Head Forward_{ avatar }"]
    modifier["Input_6"] = objects[f"Head Up_{ avatar }"]

  def add_modifier (node_groups, objects):
    mesh_list = config['mesh_list']
    
    for mesh in mesh_list:
      _add_modifier(mesh, node_groups, objects)

  data = get_data()
  node_groups = data.node_groups
  objects = data.objects
  add_modifier(node_groups, objects)

def head_origin_add_child_of (armature, head_origin_name, avatar):
  head_origin = get_object_(f'Head Origin_{ avatar }')
  # head origin 内部预先定义了一个 Child Of 约束
  constraint = head_origin.constraints.get('Child Of')
  constraint.target = armature
  constraint.subtarget = head_origin_name
  active_object_(head_origin)
  get_ops().constraint.childof_set_inverse(
    constraint = constraint.name, 
    owner='OBJECT'
  )

def rename_vertex_color (config):
  mesh_list = config['mesh_list']
  
  for mesh in mesh_list:
    # Attribute -> Col
    mesh.data.vertex_colors[0].name = 'Col'

def init_global_vars (_material_path):
  global material_path
  material_path = _material_path

def init_global_shadow (
  config, 
  armature, 
  head_origin_name, 
  material_path,
  avatar
):
  init_global_vars(material_path)
  append_objects(avatar)
  add_nodes_modifier(config, avatar)
  head_origin_add_child_of(armature, head_origin_name, avatar)
  rename_vertex_color(config)
