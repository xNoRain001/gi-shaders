# GI Shaders
[English](README.md) | [简体中文](README.zh-cn.md)


## 介绍
Blender 原神三渲二插件（基于 Festivity 的 [`Blender-miHoYo-Shaders`](https://github.com/festivize/Blender-miHoYo-Shaders)）。

## 预览
<div align="left">
  <img src="./assets/readme/preview.png" alt="preview.png" width="200"/>
  <img src="./assets/readme/preview_02.png" alt="preview_02.png" width="200"/>
</div>

## 使用

1. 下载 [`GI-Assets`](https://github.com/zeroruka/GI-Assets/tree/main/Models/Characters), 我的下载路径是 `D:\gi_assets`
<img src="./assets/readme/download-dir.png" alt="download-dir.png" />

2. [Releases](https://github.com/xNoRain001/gi-shaders/releases) 页面下载最新的 gi-shaders.zip
3. 打开 Blender (`Goo Engine v4.1.0`)
4. 安装插件 (编辑 > 偏好设置 > 安装 > 选择 gi-shaders.zip)
5. 设置材质路径
<img src="./assets/readme/config-preferences.png" alt="config-preferences.png" />

6. `重启 Blender`(改变配置后必须重启)

6. 创建一个新的 Blend 文件, 文件 -> 导入 -> FBX 
<img src="./assets/readme/import-fbx.png" alt="import-fbx.png" />

7. Alt + S 重置缩放
8. 打开侧边栏 (按下 N 键) 并且选择 `GI Shaders` 项
9. 选择角色, 骨架, head origin
<img src="./assets/readme/ui.png" alt="ui.png" />

10. 点击渲染按钮
<img src="./assets/readme/done.png" alt="done.png" />
