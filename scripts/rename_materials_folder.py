from os import rename, listdir
from os.path import join, isdir, dirname, abspath

def rename_materials_folder (base): 
  dirs = listdir(base)

  for dir in dirs:
    _base = join(base, dir)

    if isdir(_base):
      if dir == 'Material':
        rename(_base, f'{ _base }s')
      else:
        rename_materials_folder(_base)
        
dir = join(dirname(abspath(__file__)), '../assets/textures')
rename_materials_folder(dir)
