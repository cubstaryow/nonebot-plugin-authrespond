from nonebot import get_loaded_plugins, on_regex

from nonebot.adapters import Message ,Event
from nonebot.matcher import Matcher
from nonebot.permission import SUPERUSER
from nonebot.params import RegexGroup
from .cubp import cubp
from .session import  EventSession
try :
    from nonebot.adapters.onebot.v11 import Message as V11Message
except:
    V11Message = Message
    pass

turn_push = on_regex(
    r"^#([\S|-]*)(拉黑|解黑|封禁群|解禁群)([\S|-]*)$",
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
    if modulename in ["全局","all"] :
        modulename = "global"
    isgroupmode = False
    
    
    if "群" in str(args[1]):
        modulename = "group-"+modulename
        isgroupmode =True
    
    if session.platform == "qq":
        uid = V11Message(args[2].strip())
        atuid = uid['at']
    else:
        #其余平台的AT以后再说（
        atuid = []
        
        
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
    elif len(atuid) == 0:
        user_id = args[2].strip()
    else:
        user_id = atuid[0].data["qq"]


    user = user_id if user_id != "0" else "全局(插件停启用)"
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