import sys
from ..libs.blender_utils import get_operator, get_ops

# Debug
class Reload_Addon(get_operator()):
  bl_idname = "object.reload_addon"
  bl_label = "Reload Addon"

  def execute(self, context):
    addon_name = 'gi_render'
    addon_modules = [m for m in sys.modules if m.startswith(addon_name)]
    # 清空缓存
    for module_name in addon_modules:
      del sys.modules[module_name]

    # 应该先禁用插件，再清空缓存，再启动插件，但是会闪退，原因还未找到
    # 目前需要点击两次才能更新代码
    ops = get_ops()
    ops.preferences.addon_disable(module = addon_name)
    ops.preferences.addon_enable(module = addon_name)

    self.report({'INFO'}, "Addon reloaded")

    return {'FINISHED'}
