from ..libs.blender_utils import get_data, append_node_tree

def init_dissolve (dissolve_path, weapon, weapon_mesh):
  append_node_tree(dissolve_path)
  name = 'HoYoverse - Genshin Impact Weapon Dissolve'
  node_group = get_data().node_groups.get(name)
  node_group.name = name + ' ' + weapon
  modifier_name = 'Nodes Modifier For Dissolve'
  weapon_mesh.modifiers.new(type = 'NODES', name = modifier_name)
  modifier = weapon_mesh.modifiers.get(modifier_name)
  modifier.node_group = node_group
