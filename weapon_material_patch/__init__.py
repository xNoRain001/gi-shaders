from .Song_of_Broken_Pines import Song_of_Broken_Pines

strategies = {
  'Song_of_Broken_Pines': Song_of_Broken_Pines,
}

def add_weapon_material_patch (config, weapon, image_path_prefix):
  weapon = weapon.replace(' ', '_')
  
  if weapon in strategies:
    strategies[weapon](config, image_path_prefix)

  return config
