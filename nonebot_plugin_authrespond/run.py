from loguru import logger
from nonebot import get_driver
from nonebot.matcher import Matcher
from nonebot.adapters.onebot.v11 import (
    MessageEvent , GroupMessageEvent
)
from nonebot.message import  run_preprocessor
from nonebot.exception import IgnoredException
from .cubp import cubp

superusers = get_driver().config.superusers

@run_preprocessor
async def pass_rule(event: MessageEvent,matcher:Matcher):
    user_id = str(event.user_id)
    modulename = matcher.plugin.name
    if modulename.startswith("nonebot_plugin_"):
        modulename = modulename.replace("nonebot_plugin_", "")
    msg =f"plugin {modulename} is responses by {user_id}, check permission!"
    logger.opt(colors=True).debug(msg)
    if  cubp.checkperm(modulename,user_id):
        msg = f"ID {user_id} is not allow run {modulename}"
        logger.opt(colors=True).warning(msg)
        if user_id in superusers:
            return
        raise IgnoredException(msg) from None
    return True

@run_preprocessor
async def passgroup_rule(event: GroupMessageEvent,matcher:Matcher):
    group_id = str(event.group_id)
    user_id = str(event.user_id)
    modulename = matcher.plugin.name
    if modulename.startswith("nonebot_plugin_"):
        modulename = modulename.replace("nonebot_plugin_", "")
    msg =f"plugin {modulename} is responses by group {group_id}, check permission!"
    logger.opt(colors=True).debug(msg)
    if  cubp.checkpermgroup(modulename,group_id):
        msg = f"ID {group_id} group is not allow run {modulename}"
        logger.opt(colors=True).warning(msg)
        if user_id in superusers:
            return
        raise IgnoredException(msg) from None
    return True
