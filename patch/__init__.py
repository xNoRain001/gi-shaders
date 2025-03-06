from .Furina import Furina
from .Nahida import Nahida
from .material_dir_patch import material_dir_patch

strategies = {
  'Furina/Default': Furina,
  'Nahida': Nahida
}

def add_patch (config, avatar, image_path_prefix, json_path_prefix):
  if avatar in strategies:
    strategies[avatar](config, image_path_prefix, json_path_prefix)

  return config
