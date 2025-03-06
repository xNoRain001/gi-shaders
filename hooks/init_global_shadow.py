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

def add_nodes_modifier (config):
  def _add_modifier (mesh, node_groups, objects):
    modifier_name = 'Nodes Modifier For Global Shadow'
    modifier = mesh.modifiers.new(type = 'NODES', name = modifier_name)
    modifier.node_group = node_groups.get("Light Vectors")
    modifier["Input_3"] = objects["Light Direction"]
    modifier["Input_4"] = objects["Head Origin"]
    modifier["Input_5"] = objects["Head Forward"]
    modifier["Input_6"] = objects["Head Up"]

  def add_modifier (node_groups, objects):
    mesh_list = config['mesh_list']
    
    for mesh in mesh_list:
      _add_modifier(get_object_(mesh), node_groups, objects)

  data = get_data()
  node_groups = data.node_groups
  objects = data.objects
  add_modifier(node_groups, objects)

def head_origin_add_child_of (armature, head_origin_name):
  head_origin = get_object_('Head Origin')
  # head origin 内部预先定义了一个 Child Of 约束
  constraint = head_origin.constraints.get('Child Of')
  constraint.target = armature
  constraint.subtarget = head_origin_name
  active_object_(head_origin)
  get_ops().constraint.childof_set_inverse(
    constraint = constraint.name, 
    owner='OBJECT'
  )

def init_global_vars (_material_path):
  global material_path
  material_path = _material_path

def init_global_shadow (
  config, 
  armature, 
  head_origin_name, 
  material_path
):
  init_global_vars(material_path)
  append_objects()
  add_nodes_modifier(config)
  head_origin_add_child_of(armature, head_origin_name)
