from nonebot import get_driver , logger
from nonebot.matcher import Matcher
from nonebot.message import run_preprocessor
from nonebot.exception import IgnoredException
from .cubp import cubp
from nonebot_plugin_session import EventSession

superusers = get_driver().config.superusers


@run_preprocessor
async def pass_run(
    matcher: Matcher,
    session: EventSession,
):
    user_id = str(session.id1)
    await pass_rule(user_id, matcher)
    if session.level >= 2:
        await passgroup_rule(user_id, session.id2, matcher)
        if session.level == 3:
            await passgroup_rule(user_id, session.id3, matcher)
            #子ID也支持但是可能会有冲突
    pass


async def pass_rule(user_id: str, matcher: Matcher):

    modulename = matcher.plugin.name
    if modulename.startswith("nonebot_plugin_"):
        modulename = modulename.replace("nonebot_plugin_", "")
    msg = f"plugin {modulename} is responses by {user_id}, check permission!"
    logger.opt(colors=True).debug(msg)
    if cubp.checkperm(modulename, user_id):
        msg = f"ID {user_id} is not allow run {modulename}"
        logger.opt(colors=True).warning(msg)
        if user_id in superusers:
            return
        raise IgnoredException(msg) from None
    return True


async def passgroup_rule(user_id: str, group_id: str, matcher: Matcher):
    modulename = matcher.plugin.name
    if modulename.startswith("nonebot_plugin_"):
        modulename = modulename.replace("nonebot_plugin_", "")
    msg = f"plugin {modulename} is responses by group {group_id}, check permission!"
    logger.opt(colors=True).debug(msg)
    if cubp.checkpermgroup(modulename, group_id):
        msg = f"ID {group_id} group is not allow run {modulename}"
        logger.opt(colors=True).warning(msg)
        if user_id in superusers:
            return
        raise IgnoredException(msg) from None
    return True
