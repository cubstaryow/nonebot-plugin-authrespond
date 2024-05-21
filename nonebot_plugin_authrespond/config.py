from nonebot import get_driver
from pydantic import BaseModel


class cubplugins_permission(BaseModel):
    cubplugin_datadir : str=""
config: cubplugins_permission = cubplugins_permission.parse_obj(get_driver().config.dict())
