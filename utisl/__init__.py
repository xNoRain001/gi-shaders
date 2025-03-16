from ..const import bl_idname

def get_preferences (context):
  pass

def get_texture_dir (context):
  addons = context.preferences.addons

  if bl_idname in addons:
    return addons[bl_idname].preferences.texture_dir
  
  return ''

def get_weapon_texture_dir (context):
  addons = context.preferences.addons

  if bl_idname in addons:
    return addons[bl_idname].preferences.weapon_texture_dir
  
  return ''

def get_language (context):
  addons = context.preferences.addons

  if bl_idname in addons:
    return addons[bl_idname].preferences.language
  
  return ''

