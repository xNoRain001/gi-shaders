from os.path import exists
from ..libs.blender_utils import get_data, get_material, get_object_

from ..const import material_prefix

# 不清空有可能会导致未知的问题
def reset_uv_map (materials):
  for material in materials:
    nodes = material.node_tree.nodes
    node_name = "UV Map"

    if node_name in nodes:
      nodes[node_name].uv_map = ""

def import_materials (material_path):
  # Body Face Hair Outlines
  with get_data().libraries.load(material_path, link = False) as (data_from, data_to):
    data_to.materials = data_from.materials

  reset_uv_map(data_to.materials)

def init_body_type (config):
  node = get_data().materials[f'{ material_prefix }Face'].node_tree.nodes['Face Shader']
  node.inputs[0].default_value = config['body_type']

def related_materials (armature, config):
  objects = armature.children
  material_map = config['material_map']  

  for object in objects:
    if object.type == 'MESH':
      materials = object.data.materials

      for index, material in enumerate(materials):
        suffix = material.name.split('_')[-1]

        if suffix in material_map:
          materials[index] = get_material(material_map[suffix])

def get_node (data, body_type, node_name, image_type):
  if image_type == 'shadow_ramp':
    # 去节点组内寻找
    # Body_Shadow_Ramp -> Body Shadow Ramp
    node = data.node_groups[node_name.replace('_', ' ')].nodes[node_name]
  else:
    node = get_material(material_prefix + body_type).node_tree.nodes[node_name]

  return node

def _node_set_image (data, node, image_path, image_type):
  image = data.images.load(image_path)
  image.alpha_mode = 'CHANNEL_PACKED'

  if image_type == 'lightmap' or image_type == 'normalmap':
    image.colorspace_settings.name = 'Non-Color'

  node.image = image

def node_set_image (body_type, node_name, image_path, image_type):
  # 3.0 之前不存在法向贴图
  if not exists(image_path):
    return
  
  data = get_data()
  node = get_node(data, body_type, node_name, image_type)
  _node_set_image(data, node, image_path, image_type)

def __init_materials (materials):
  for key, image_path in materials.items():
    body_type, node_name, image_type = key.split(':')
    node_set_image(body_type, node_name, image_path, image_type)

def _init_materials (config):
  materials = config['materials']
  __init_materials(materials)
  init_body_type(config)

def rename_vertex_color (config):
  mesh_list = config['mesh_list']
  
  for mesh_name in mesh_list:
    # Attribute -> Col
    get_object_(mesh_name).data.vertex_colors[0].name = 'Col'

def gen_extra_materials (config):
  extra_materials = config['extra_materials']

  for extra_material in extra_materials:
    target, source = extra_material.split(':')
    material = get_material(material_prefix + source)
    new_material = material.copy()
    new_material.name = material_prefix + target

def init_materials (
  armature, 
  material_path, 
  config
):
  import_materials(material_path)
  gen_extra_materials(config)
  _init_materials(config)
  related_materials(armature, config)
  rename_vertex_color(config)
