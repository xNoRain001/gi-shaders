from os import path, rename, listdir

join = path.join
dirname = path.dirname
abspath = path.abspath

suffix_list = [
  'Tex_Face_Diffuse.png',
  'Tex_Body_Diffuse.png',
  'Tex_Body_Lightmap.png',
  'Tex_Body_Normalmap.png',
  'Tex_Body_Shadow_Ramp.png',
  'Tex_Hair_Diffuse.png',
  'Tex_Hair_Lightmap.png',
  'Tex_Hair_Normalmap.png',
  'Tex_Hair_Shadow_Ramp.png',
  'Tex_EffectHair_Diffuse.png',
  'Tex_EffectHair_Lightmap.png'
]

# Avatar_Girl_Sword_Furina_Tex_Body_Diffuse.png -> Body_Diffuse.png
def rename_textures ():
  base = join(dirname(abspath(__file__)), '../assets/textures')
  dirs = listdir(base)
  
  for dir in dirs:
    _base = join(base, f'./{ dir }')
    file_names = listdir(_base)

    for file_name in file_names:
      for suffix in suffix_list:
        if file_name.endswith(suffix):
          old_name = join(_base, file_name)
          new_name = join(_base, suffix[4:])
          rename(old_name, new_name)

          break

rename_textures()
