from ..const import bl_idname

def get_texture_dir (context):
  return context.preferences.addons[bl_idname].preferences.texture_dir
