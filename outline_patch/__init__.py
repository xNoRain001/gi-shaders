from .Furina import Furina
from .Nahida import Nahida
from .material_dir_patch import material_dir_patch

strategies = {
  'Furina/Default': Furina,
  'Nahida': Nahida
}

def add_outline_patch (config, avatar, json_path_prefix):
  if avatar in strategies:
    strategies[avatar](config, json_path_prefix)

  return config
