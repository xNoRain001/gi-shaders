from ..libs.blender_utils import get_data, get_material

def related_materials (material, weapon_mesh):
  materials = weapon_mesh.data.materials

  for index, _ in enumerate(materials):
    materials[index] = material

def _init_materials (config, material):
  materials = config['materials']
  nodes = material.node_tree.nodes
  
  for key, image_path in materials.items():
    suffix, node_name = key.split(':')
    node = nodes[node_name]
    image = get_data().images.load(image_path)
    node.image = image

def init_node_config (material):
  inputs = material.node_tree.nodes["Body Shader"].inputs
  inputs[0].default_value = 1

  for i in range(28, 38):
    inputs[i].default_value = (1, 1, 1, 1)

def import_materials (material_path, material_name = None, new_material_name = None):
  with get_data().libraries.load(material_path, link = False) as (data_from, data_to):
    if material_name:
      for material in data_from.materials:
        if material == material_name:
          data_to.materials.append(material)

          break
    else:
      data_to.materials = data_from.materials

  if new_material_name:
    data_to.materials[0].name = new_material_name

  return data_to.materials[0]

def init_weapon_materials (
  material_path, 
  config,
  weapon,
  weapon_mesh
):
  # 多导入了 Face Body
  material_name = 'HoYoverse - Genshin Weapons'
  new_material_name = f'{ material_name } - { weapon }'
  material = import_materials(material_path, material_name, new_material_name)
  init_node_config(material)
  _init_materials(config, material)
  related_materials(material, weapon_mesh)
