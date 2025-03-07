bl_info = {
  "name": "GI Shaders",
  "blender": (4, 1, 0),
  "category": "Render",
}

from .libs.blender_utils import (
  register as utils_register, 
  unregister as utils_unregister,
  get_context
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

if __name__ == "__main__":
  register()
