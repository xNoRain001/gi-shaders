from .Furina import Furina
from .Nahida import Nahida
from .Xiao import Xiao
from .Lynette import Lynette

strategies = {
  'Furina/Default': Furina,
  'Nahida/Default': Nahida,
  'Xiao/Default': Xiao,
  'Lynette/Default': Lynette,
}

def add_material_patch (config, avatar, image_path_prefix):
  if avatar in strategies:
    strategies[avatar](config, image_path_prefix)

  return config
