from ..libs.blender_utils import (
  get_props, 
  get_panel, 
  add_row_with_operator, 
  add_row_with_label, 
  add_scene_custom_prop,
  get_operator_file_list_element,
)

class GI_Render (get_panel()):
  bl_space_type = 'VIEW_3D'
  bl_region_type = 'UI'
  bl_category = "Item"
  bl_label = "GI Render"
  bl_idname = "_PT_GI_Render_PT_"

  files: get_props().CollectionProperty(type=get_operator_file_list_element())

  def invoke(self, context, event):
    wm = context.window_manager

    return wm.invoke_props_dialog(self)

  def draw(self, context):
    layout = self.layout
    scene = context.scene
    factor = .3
    mytool = scene.my_tool

    # For test
    # setattr(mytool, 'textures_dir', 'D:\gi_assets\Lumine\\')
    # setattr(mytool, 'materials_dir', 'D:\gi_assets\Lumine\Materials\\')

    add_row_with_label(layout, '体型:', scene, 'body_type', factor)
    add_row_with_label(layout, '光照贴图目录:', mytool, 'textures_dir', factor)
    add_row_with_label(layout, 'Material 目录:', mytool, 'materials_dir', factor)
 
    layout.operator("wm.select_face_files")
    for file_path in mytool.face_files_path:
      layout.label(text=file_path.name)
    
    layout.operator("wm.select_body_files")
    for file_path in mytool.body_files_path:
      layout.label(text=file_path.name)

    layout.operator("wm.select_hair_files")
    for file_path in mytool.hair_files_path:
      layout.label(text=file_path.name)

    add_row_with_operator(layout, 'object.render', '开始渲染')

add_scene_custom_prop(
  'body_type', 
  'Int', 
  3, 
  'Loli / Boy / Girl / Male / Lady => [1, 5]',
  1,
  5
)
