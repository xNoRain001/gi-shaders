from .Xiao import Xiao
from .Furina import Furina
from .Nahida import Nahida
from .Lynette import Lynette
from .Mavuika import Mavuika

strategies = {
  'Xiao/Default': Xiao,
  'Furina/Default': Furina,
  'Nahida/Default': Nahida,
  'Lynette/Default': Lynette,
  'Mavuika/Default': Mavuika,
}

def add_material_patch (config, avatar, image_path_prefix):
  if avatar in strategies:
    strategies[avatar](config, image_path_prefix)

  return config
