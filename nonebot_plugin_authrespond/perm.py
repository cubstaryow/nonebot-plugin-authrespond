from nonebot import get_loaded_plugins, on_regex

from nonebot.adapters import Message ,Event
from nonebot.matcher import Matcher
from nonebot.permission import SUPERUSER
from nonebot.params import RegexGroup
from .cubp import cubp
from nonebot_plugin_session import EventSession
from nonebot_plugin_alconna import UniMessage , At

turn_push = on_regex(
    r"^#([\S|-]*)(拉黑|解黑|封禁群|解禁群|去群白|去白|加白|加群白)([\S|-]*)$",
    block=True,
    priority=2,
    permission=SUPERUSER
)
@turn_push.handle()
async def _(
    event:Event,
    matcher : Matcher,
    session: EventSession,
    args : list = RegexGroup(),
):
    
    modulename = args[0]
    
    if modulename.startswith("nonebot_plugin_"):
        modulename = modulename.replace("nonebot_plugin_", "")
    pluginslist = await getpluginslist()
    if  modulename not in pluginslist and modulename not in ["全局","all"]:
        await matcher.finish("[Failed]不存在此模块")
    themodulename = modulename
    if modulename in ["全局","all"] :
        modulename = "global"
    isgroupmode = False
    

    if "群" in str(args[1]):
        modulename = "group-"+modulename
        isgroupmode =True

    if "白" in str(args[1]):
        modulename = "!-"+modulename

    uni_msg = UniMessage()
    if args[2]:
        msg: Message = event.get_message()
        uni_msg = UniMessage.generate_without_reply(message=msg)
    atuid = uni_msg.get(At)

    if args[2] =="":
        if isgroupmode:
            if session.level >=2:
                user_id = str(session.id2)
            else:
                await matcher.finish("[Failed]群组操作模式下缺失关键参数")
        else:
            await matcher.finish("[Failed]用户操作模式下缺失关键参数")
    elif  args[2] in ["全员","全体成员" , "all"]:
        if isgroupmode:
            await matcher.finish("[Failed]群组操作模式下无法操作全体(虽然支持但是请使用用户模式)")
        else:
            user_id = "0"
            if modulename.startswith("!-"):
                await matcher.finish("[Failed]白名单无法应用于全局(对象)")
    elif len(atuid) == 0:
        user_id = args[2].strip()
    else:
        atmsg :At= atuid[0]
        user_id = atmsg.target


    user = user_id if user_id != "0" else "全局(插件停启用)"
    user = "群"+user if isgroupmode else user
    check = False
    mode="禁止"
    if str(args[1]) in ["解黑","解禁群"]:
        check = True
        mode="允许"
    if "白" in str(args[1]):
        mode="始终允许(忽略黑名单)"
        if "去" in str(args[1]):
            mode="重新设定(去白名单)"
            check = True
        
        
    ret = cubp.setperm(modulename,user_id,check)
    
    
    msg = f"[cubp-W]操作失败,可能已经{str(args[1])}"
    if ret:
        msg = f"[cubp-I]已{mode}{themodulename}响应{user}"
    await matcher.finish(msg)
    
async def getpluginslist():
    """获取插件列表
        return: list[pluginname]
    """
    plugin_set = get_loaded_plugins()
    plugin_names = []
    for plugin in plugin_set:
        if plugin.name.startswith("nonebot_plugin_"):
            plugin_names.append(plugin.name.replace("nonebot_plugin_", ""))
        else:
            plugin_names.append(plugin.name)
    return plugin_names