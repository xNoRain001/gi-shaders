from ..libs.blender_utils import (
  get_props, 
  get_panel, 
  add_row_with_operator, 
  add_row_with_label, 
  get_operator_file_list_element,
  get_property_group
)

class VIEW3D_PT_render (get_panel()):
  bl_space_type = 'VIEW_3D'
  bl_region_type = 'UI'
  bl_category = "Item"
  bl_label = "GI Render"
  bl_idname = "VIEW3D_PT_render"

  files: get_props().CollectionProperty(type=get_operator_file_list_element())

  def invoke(self, context, event):
    wm = context.window_manager

    return wm.invoke_props_dialog(self)

  def draw(self, context):
    layout = self.layout
    scene = context.scene
    factor = 0.3
    file_config = scene.file_config

    # TODO: 光照界面
    # row = layout.row()
    # row.prop(scene, 'light_direction_x', text = 'X')

    # row = layout.row()
    # row.prop(scene, 'light_direction_y', text = 'Y')

    # row = layout.row()
    # row.prop(scene, 'light_direction_z', text = 'Z')

    row = layout.row()
    row.prop(scene, 'mesh_name', text = 'mesh 名称')
    row = layout.row()
    row.prop(scene, 'armature_name', text = '骨架名称')
    row = layout.row()
    row.prop(scene, 'head_bone_name', text = '脸部阴影跟随目标')
 
    add_row_with_label(layout, '体型:', scene, 'body_type', factor)
    add_row_with_label(layout, '光照贴图目录:', file_config, 'textures_dir', factor)
    add_row_with_label(layout, 'Material 目录（用于描边颜色）:', file_config, 'materials_dir', factor)
 
    row = layout.row()
    row.operator("object.select_face_files")
    row.operator("object.select_body_files")
    row.operator("object.select_hair_files")
    row = layout.row()
    col = row.column()
    for file_path in file_config.face_files_path:
      col.label(text = file_path.name)
    col = row.column()
    for file_path in file_config.body_files_path:
      col.label(text = file_path.name)
    col = row.column()
    for file_path in file_config.hair_files_path:
      col.label(text = file_path.name)

    add_row_with_operator(layout, 'object.render', '开始渲染')
