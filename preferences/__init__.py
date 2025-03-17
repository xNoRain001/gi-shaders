from ..libs.blender_utils import (
  register_classes, 
  unregister_classes, 
  get_props, 
  get_types
)

from ..const import bl_idname

class Preferences (get_types('AddonPreferences')):
  bl_idname = bl_idname

  texture_dir: get_props().StringProperty(
    name = 'texture_dir',
    subtype = 'DIR_PATH',
    default = 'D:\\gi-assets2\\Characters' # For test
  )
  weapon_texture_dir: get_props().StringProperty(
    name = 'weapon_texture_dir',
    subtype = 'DIR_PATH',
    default = 'D:\\gi-assets2\\Weapons' # For test
  )
  language: get_props().EnumProperty(
    name = 'language',
    items = [
       ('ZH', 'ZH', ''),
       ('EN', 'EN', '')
    ]
  )

  def draw(self, context):
    layout = self.layout
    row = layout.row()
    row.prop(self, 'texture_dir', text = 'Texture Dir')
    row = layout.row()
    row.prop(self, 'weapon_texture_dir', text = 'Weapon Texture Dir')
    row = layout.row()
    row.prop(self, 'language', text = 'Language')

classes = (Preferences, )

def register():
  register_classes(classes)
  
def unregister():
  unregister_classes(classes)
