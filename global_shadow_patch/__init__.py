from .Furina import Furina

strategies = {
  'Furina/Default': Furina
}

def add_global_shadow_patch (config, avatar):
  if avatar in strategies:
    strategies[avatar](config)

  return config
