from .utils import add_outline_colors

def Song_of_Broken_Pines (config, json_path_prefix):
  config['outline_colors']['Weapons'] = config['outline_colors']['Weapons'].replace('_Mat', '_Mat_Eff')
