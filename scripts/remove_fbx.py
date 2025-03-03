from os import path, remove, listdir

join = path.join
dirname = path.dirname
abspath = path.abspath
splitext = path.splitext

def remove_fbx ():
  base = join(dirname(abspath(__file__)), '../assets/textures')
  dirs = listdir(base)
  
  for dir in dirs:
    _base = join(base, f'./{ dir }')
    file_names = listdir(_base)

    for file_name in file_names:
      _, file_extension = splitext(file_name)
      
      if file_extension == '.fbx':
        remove(join(_base, file_name))

remove_fbx()
