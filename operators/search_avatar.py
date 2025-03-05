from ..libs.blender_utils import get_operator

class OBJECT_OT_Search_Avatar (get_operator()):
  bl_idname = "object.search_avatar"
  bl_label = "Search Avatar"

  def execute(self, context):
    return {'FINISHED'}

  def invoke(self, context, event):
    context.window_manager.invoke_search_popup(self)

    return {'RUNNING_MODAL'}
