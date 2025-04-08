def add_meshes (armature, config, meshes):
  children = armature.children

  if not isinstance(meshes, list):
    meshes = [meshes]

  for mesh in meshes:
    for child in children:
      if child.type == 'MESH':
        name = child.name

        if name.startswith(mesh):
          config['mesh_list'].append(child)

          break
