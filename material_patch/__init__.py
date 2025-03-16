from .Furina import Furina
from .Nahida import Nahida

strategies = {
  'Furina/Default': Furina,
  'Nahida': Nahida
}

def add_material_patch (config, avatar, image_path_prefix):
  if avatar in strategies:
    strategies[avatar](config, image_path_prefix)

  return config
