from ..libs.blender_utils import get_property_group, get_props

class File_Config (get_property_group()):
  textures_dir: get_props().StringProperty(
    name="textures_dir",
    subtype='DIR_PATH',
    # for test
    default='D:\gi_assets\Lumine\\'
  )
  materials_dir: get_props().StringProperty(
    name="materials_dir",
    subtype='DIR_PATH',
    # for test
    default='D:\gi_assets\Lumine\Materials\\'
  )
  face_files_path: get_props().CollectionProperty(
    name="face_files_path",
    type=get_property_group()
  )
  body_files_path: get_props().CollectionProperty(
    name="body_files_path",
    type=get_property_group()
  )
  hair_files_path: get_props().CollectionProperty(
    name="hair_files_path",
    type=get_property_group()
  )
