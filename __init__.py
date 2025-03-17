bl_info = {
  'name': 'GI Shaders',
  'author': 'xNoRain001',
  'version': (0, 0, 2),
  'blender': (4, 1, 0),
  'location': 'View3D > Sidebar > GI Shaders',
  'category': 'Render',
  'description': 'Blender addons for Genshin Impact shaders.',
  'doc_url': 'https://github.com/xNoRain001/gi-shaders',
  'tracker_url': 'https://github.com/xNoRain001/gi-shaders/issues'
}

from .libs.blender_utils import (
  register as utils_register, 
  unregister as utils_unregister
)
from .panels import (
  register as panels_register, 
  unregister as panels_unregister
)
from .operators import (
  register as operators_register, 
  unregister as operators_unregister
)
from .scene import (
  register as scene_register, 
  unregister as scene_unregister
)
from .preferences import (
  register as preferences_register,
  unregister as preferences_unregister,
)

def register():
  preferences_register()
  utils_register()
  operators_register()
  panels_register()
  scene_register()

def unregister():
  preferences_unregister()
  utils_unregister()
  panels_unregister()
  operators_unregister()
  scene_unregister()

if __name__ == '__main__':
  register()
