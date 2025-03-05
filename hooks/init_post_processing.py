from ..libs.blender_utils import get_data, get_context, append_node_tree

def link_post_processing (node_tree):
  nodes = node_tree.nodes
  links = node_tree.links
  composite, render_layers, post_processing = nodes
  links.new(render_layers.outputs[0], post_processing.inputs[0])
  links.new(post_processing.outputs[0], composite.inputs[0])

  return node_tree

def init_compositor ():
  node_tree = get_data().node_groups.get('HoYoverse - Post Processing')
  scene = get_context().scene
  scene.use_nodes = True
  _node_tree = scene.node_tree
  _node_tree.nodes.new(type='CompositorNodeGroup').node_tree = node_tree

  return _node_tree

def init_post_processing (post_processing_path):
  append_node_tree(post_processing_path)
  node_tree = init_compositor()
  link_post_processing(node_tree)
  get_context().scene.view_settings.view_transform = 'Standard'
