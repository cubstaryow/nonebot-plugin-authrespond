from nonebot import get_loaded_plugins, on_regex
from nonebot.adapters.onebot.v11 import(
    Bot,
    Message,
    MessageEvent,
    GroupMessageEvent
)
from nonebot.matcher import Matcher
from nonebot.permission import SUPERUSER
from nonebot.params import RegexGroup
from .cubp import cubp

turn_push = on_regex(
    r"^#(.*)(拉黑|解黑|封禁群|解禁群)(.*)$",
    block=True,
    priority=2,
    permission=SUPERUSER
)
@turn_push.handle()
async def _(
    event : MessageEvent,
    matcher : Matcher,
    args : list = RegexGroup(),
):
    modulename = args[0]
    if modulename.startswith("nonebot_plugin_"):
        modulename = modulename.replace("nonebot_plugin_", "")
    pluginslist = await getpluginslist()
    if  modulename not in pluginslist and modulename not in ["全局","all"]:
        await matcher.finish("[Failed]不存在此模块")
    if modulename in ["全局","all"] :
        modulename = "global"
    isgroupmode = False
    if "群" in str(args[1]):
        modulename = "group-"+modulename
        isgroupmode =True
    
    uid = Message(args[2].strip())
    if args[2] =="":
        if isgroupmode:
            if isinstance(event , GroupMessageEvent):
                user_id = str(event.group_id)
            else:
                await matcher.finish("[Failed]群组操作模式下缺失关键参数")
        else:
            await matcher.finish("[Failed]用户操作模式下缺失关键参数")
    elif  args[2] in ["全员","全体成员" , "all"]:
        if isgroupmode:
            await matcher.finish("[Failed]群组操作模式下无法操作全体(虽然支持但是请使用用户模式)")
        else:
            user_id = "0"
    elif len(uid['at']) == 0:
        user_id = args[2].strip()
    else:
        user_id = uid['at'][0].data["qq"]

    user = user_id if user_id != "0" else "全局(插件停用)"
    user = "群"+user if isgroupmode else user
    check = False
    mode="禁止"
    if str(args[1]) in ["解禁","解黑","解禁群"]:
        check = True
        mode="允许"
    ret = cubp.setperm(modulename,user_id,check)
    msg = f"[cubp-W]操作失败,可能已经{str(args[1])}"
    if ret:
        msg = f"[cubp-I]已{mode}{modulename}响应{user}"
    await matcher.finish(msg)
    
async def getpluginslist():
    plugin_set = get_loaded_plugins()
    plugin_names = []
    for plugin in plugin_set:
        if plugin.name.startswith("nonebot_plugin_"):
            plugin_names.append(plugin.name.replace("nonebot_plugin_", ""))
        else:
            plugin_names.append(plugin.name)
    return plugin_names