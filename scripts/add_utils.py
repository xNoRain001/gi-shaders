import sys
import subprocess

def add_utils ():
  subprocess.run(
    [
      sys.executable, 
      "-m", 
      "pip", 
      "install", 
      "blender_utils", 
      "--target",
      # "C:\Users\xNoRain\AppData\Roaming\Blender Foundation\Blender\4.2\scripts\addons\gi-shaders\libs"
      "D:\\blender4.1\\4.1\scripts\\addons\\gi-shaders\\libs"
    ],
    check=True, 
    stdout=subprocess.PIPE, 
    stderr=subprocess.PIPE, 
    text=True
  )

add_utils()
