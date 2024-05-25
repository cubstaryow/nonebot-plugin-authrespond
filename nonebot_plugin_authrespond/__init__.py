from nonebot import require
require("nonebot_plugin_session")
require("nonebot_plugin_alconna")
require("nonebot_plugin_localstore")
from nonebot.plugin import PluginMetadata
from .config import cubplugins_permission
from nonebot.plugin import inherit_supported_adapters

__plugin_meta__ = PluginMetadata(
    name="插件响应鉴权",
    description="nonebot简单易用的黑名单插件，实现分插件拉黑用户/群聊/全局",
    usage='''用户操作模式:  #(全局|插件名称)(拉黑|解黑)(全员|用户id)
群聊操作模式: #(全局|插件名称)(封禁群|解禁群)(群号|留空封禁所在群)''',

    type="application",
    # 发布必填，当前有效类型有：`library`（为其他插件编写提供功能），`application`（向机器人用户提供功能）。

    homepage="https://github.com/cubstaryow/nonebot-plugin-authrespond",
    # 发布必填。

    config=cubplugins_permission,
    # 插件配置项类，如无需配置可不填写。
    supported_adapters=inherit_supported_adapters(
        "nonebot_plugin_alconna",
        "nonebot_plugin_session",
        "nonebot_plugin_localstore"
    )
    # 支持的适配器集合，其中 `~` 在此处代表前缀 `nonebot.adapters.`，其余适配器亦按此格式填写。
    # 若插件可以保证兼容所有适配器（即仅使用基本适配器功能）可不填写，否则应该列出插件支持的适配器。
)

from .run import *

from .perm import *
