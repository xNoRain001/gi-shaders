from os import remove, listdir
from os.path import join, isdir, dirname, abspath, splitext

def remove_fbx (base): 
  dirs = listdir(base)

  for dir in dirs:
    _base = join(base, dir)

    if isdir(_base):
      remove_fbx(_base)
    else:
      _, file_extension = splitext(dir)
        
      if file_extension == '.fbx':
        remove(_base)

dir = join(dirname(abspath(__file__)), '../assets/textures')
remove_fbx(dir)
