from .Furina import Furina

strategies = {
  'Furina/Default': Furina
}

def add_global_shadow_patch (armature, config, avatar):
  if avatar in strategies:
    strategies[avatar](armature, config)

  return config
