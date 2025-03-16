# GI Shaders
[English](README.md) | [简体中文](README.zh-cn.md)

## Introduction
Blender addon for Genshin Impact shaders (based on Festivity's [`Blender-miHoYo-Shaders`](https://github.com/festivize/Blender-miHoYo-Shaders)) .

## Preview
<div align="left">
  <img src="./assets/readme/preview.png" alt="preview.png" width="200"/>
  <img src="./assets/readme/preview_02.png" alt="preview_02.png" width="200"/>
  <img src="./assets/readme/weapon.png" alt="weapon.png" width="200"/>
</div>

## Usage

### Render avatar

1. Download [`GI-Assets`](https://github.com/zeroruka/GI-Assets/tree/main/Models/Characters), My download dir is `D:\gi_assets\Characters`(Download as needed)
<img src="./assets/readme/download-dir.png" alt="download-dir.png" />

2. Go to the [Releases](https://github.com/xNoRain001/gi-shaders/releases) page and download the latest gi-shaders.zip
3. Open Blender (`Goo Engine v4.1.0`)
4. Install Addon (Edit > Preferences > Install > Select gi-shaders.zip)
5. Config preferences, texture dir choose download assets dir
<img src="./assets/readme/config-preferences.png" alt="config-preferences.png" />

6. `Restart blend`(After change texture dir, must restart.)

6. Create new blend file and import model, File -> Import -> FBX 
<img src="./assets/readme/import-fbx.png" alt="import-fbx.png" />

7. Alt + S to reset model size
8. Open up the N-Panel (Hit the 'N' key) and select the `GI Shaders` tab
9. Choose avatar, armature, head origin
<img src="./assets/readme/ui.png" alt="ui.png" />

10. Click render button
<img src="./assets/readme/done.png" alt="done.png" />

### Render weapon

1. Download [`GI-Assets`](https://github.com/Hoyotoon/HoyoToon-Assets/tree/main/Genshin%20Impact/Weapons), My download dir is `D:\gi_assets\Weapons`(Download as needed)
<img src="./assets/readme/download-dir-2.png" alt="download-dir-2.png" />

2. Render
<img src="./assets/readme/render-weapon.png" alt="render-weapon.png" />
