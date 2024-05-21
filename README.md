<div align="center">
  <a href="https://v2.nonebot.dev/store"><img src="https://github.com/cubstaryow/nonebot-plugin-authrespond/blob/master/.github/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>
  <br>
  <p><img src="https://github.com/cubstaryow/nonebot-plugin-authrespond/blob/master/.github/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText"></p>
</div>

<div align="center">

<div align="center">

# nonebot-plugin-authrespond

_✨ nonebot简单易用的黑名单插件，实现分插件拉黑用户/群聊/全局 ✨_


<a href="./LICENSE">
    <img src="https://img.shields.io/github/license/owner/nonebot-plugin-authrespond.svg" alt="license">
</a>
<a href="https://pypi.python.org/pypi/nonebot-plugin-authrespond">
    <img src="https://img.shields.io/pypi/v/nonebot-plugin-authrespond.svg" alt="pypi">
</a>
<img src="https://img.shields.io/badge/python-3.10+-blue.svg" alt="python">

</div>


## 📖 介绍

简单易用的黑名单插件，实现分插件拉黑用户/群聊/全局,无需修改插件源码

原理为插件运行前监听Matcher响应器属性

## 💿 安装

<details open>
<summary>使用 nb-cli 安装</summary>
在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装

    nb plugin install nonebot-plugin-authrespond

</details>

<details>
<summary>使用包管理器安装</summary>
在 nonebot2 项目的插件目录下, 打开命令行, 根据你使用的包管理器, 输入相应的安装命令

<details>
<summary>pip</summary>

    pip install nonebot-plugin-authrespond
</details>
<details>
<summary>pdm</summary>

    pdm add nonebot-plugin-authrespond
</details>
<details>
<summary>poetry</summary>

    poetry add nonebot-plugin-authrespond
</details>
<details>
<summary>conda</summary>

    conda install nonebot-plugin-authrespond
</details>

打开 nonebot2 项目根目录下的 `pyproject.toml` 文件, 在 `[tool.nonebot]` 部分追加写入

    plugins = ["nonebot_plugin_authrespond"]

</details>

## ⚙️ 配置

在 nonebot2 项目的`.env`文件中添加下表中的必填配置

| 配置项 | 必填 | 默认值 | 说明 |
|:-----:|:----:|:----:|:----:|
| cubplugin_datadir | 否 | "" | 自定义配置文件路径,默认localstore |


## 🎉 使用
### 指令表
| 指令 | 权限 | 需要@ | 范围 | 说明 |
|:-----:|:----:|:----:|:----:|:----:|
| #(全局|插件名称)(拉黑|解黑)(全员|用户id) | 主人 | 否 | 私聊/群聊 | 用户操作模式 |
| #(全局|插件名称)(封禁群|解禁群)(群号|留空封禁所在群) | 主人 | 否 | 私聊/群聊 | 群聊操作模式 |


