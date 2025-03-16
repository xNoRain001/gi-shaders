from os.path import exists
from ..libs.blender_utils import get_data, get_material

from ..const import material_prefix

# 不清空有可能会导致未知的问题
def reset_uv_map (materials):
  for material in materials:
    nodes = material.node_tree.nodes
    node_name = "UV Map"

    if node_name in nodes:
      nodes[node_name].uv_map = ""

def init_body_type (config):
  node = get_data().materials[material_prefix + 'Face'].node_tree.nodes['Face Shader']
  node.inputs[0].default_value = config['body_type']

def init_node_config ():
  inputs = get_material('HoYoverse - Genshin Weapons').node_tree.nodes["Body Shader"].inputs
  inputs[0].default_value = 1

  for i in range(28, 38):
    inputs[i].default_value = (1, 1, 1, 1)

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

def _init_materials (config, is_weapon):
  materials = config['materials']
  __init_materials(materials)

  if is_weapon:
    init_node_config()
  else:
    init_body_type(config)

def gen_extra_materials (config):
  extra_materials = config['extra_materials']

  for extra_material in extra_materials:
    target, source = extra_material.split(':')
    material = get_material(material_prefix + source)
    new_material = material.copy()
    new_material.name = material_prefix + target

def import_materials (material_path, is_weapon):
  with get_data().libraries.load(material_path, link = False) as (data_from, data_to):
    if is_weapon:
      for material in data_from.materials:
        if material == 'HoYoverse - Genshin Weapons' or material == 'HoYoverse - Genshin Outlines':
          data_to.materials.append(material)
    else:
      data_to.materials = data_from.materials

  return data_to.materials

def init_materials (
  armature, 
  material_path, 
  config,
  is_weapon = False
):
  materials = import_materials(material_path, is_weapon)
  reset_uv_map(materials)
  gen_extra_materials(config)
  _init_materials(config, is_weapon)
  related_materials(armature, config)
