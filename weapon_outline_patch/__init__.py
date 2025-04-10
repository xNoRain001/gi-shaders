from .Song_of_Broken_Pines import Song_of_Broken_Pines

strategies = {
  'Song_of_Broken_Pines': Song_of_Broken_Pines,
}

def add_weapon_outline_patch (config, weapon, json_path_prefix):
  weapon = weapon.replace(' ', '_')

  if weapon in strategies:
    strategies[weapon](config, json_path_prefix)

  return config
