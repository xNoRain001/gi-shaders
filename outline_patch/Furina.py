from .utils import add_outline_material, add_outline_slot

def Furina (config, json_path_prefix):
  add_outline_material(config, 'Hair', 'Effect', json_path_prefix)
  add_outline_slot(config, 'EffectHair', ['Other', 'Effect', 'Effect'])
