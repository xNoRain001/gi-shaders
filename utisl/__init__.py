from ..const import bl_idname

def get_texture_dir (context):
  addons = context.preferences.addons

  if bl_idname in addons:
    return addons[bl_idname].preferences.texture_dir
  
  return ''
