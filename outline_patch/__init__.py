from .Furina import Furina
from .Nahida import Nahida
from .Lynette import Lynette
from .Citlali import Citlali

strategies = {
  'Furina/Default': Furina,
  'Nahida/Default': Nahida,
  'Lynette/Default': Lynette,
  'Citlali/Default': Citlali,
}

def add_outline_patch (config, avatar, json_path_prefix):
  if avatar in strategies:
    strategies[avatar](config, json_path_prefix)

  return config
