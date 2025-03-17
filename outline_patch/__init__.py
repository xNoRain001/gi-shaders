from .Furina import Furina
from .Nahida import Nahida

strategies = {
  'Furina/Default': Furina,
  'Nahida/Default': Nahida,
}

def add_outline_patch (config, avatar, json_path_prefix):
  if avatar in strategies:
    strategies[avatar](config, json_path_prefix)

  return config
