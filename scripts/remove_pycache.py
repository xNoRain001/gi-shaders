from os import walk
import shutil
from os.path import join, dirname, abspath

def remove_pycache(directory):
  for root, dirs, files in walk(directory):
    for dir_name in dirs:
      if dir_name == "__pycache__":
          dir_path = join(root, dir_name)
          shutil.rmtree(dir_path)

dir = join(dirname(abspath(__file__)), '../../gi-shaders')
remove_pycache(dir)
