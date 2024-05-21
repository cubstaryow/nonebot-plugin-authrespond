from loguru import logger
from .plugins_data import wdata , rdata ,initdata ,driver
conf_name="cubplugins_permission.json"
bashdata={'global':[],'group-global':[]}
initdata(conf_name,bashdata)


class cubplugins_permission:
    cubplugins_P = rdata(conf_name)

    def __init__(self):
        pass
    
    def savedata(self):
        wdata(conf_name,self.cubplugins_P)
    
    def checkperm(self , modulename:str , user_id:str ):
        globaldata = self.cubplugins_P.get('global',[])
        if user_id in globaldata:
            return True
        if self.cubplugins_P.get(modulename,None) == None:
            return False
        data = self.cubplugins_P[modulename]
        if user_id in data or '0' in data:
            return True
        return False
    
    def checkpermgroup(self , modulename:str , group_id:str ):
        groupdata = self.cubplugins_P.get('group-global',[])
        if group_id in groupdata:
            return True
        if self.cubplugins_P.get('group-'+modulename,None) == None:
            return False
        data = self.cubplugins_P['group-'+modulename]
        if group_id in data:
            return True
        return False
    
    def setperm(self , modulename:str , user_id:str , allow : bool =False):
        if self.cubplugins_P.get(modulename,None) == None:
            self.cubplugins_P[modulename] =[]
        data = self.cubplugins_P[modulename]
        check = False
        if allow:
            if user_id in data:
                data.remove(user_id)
                check = True
        else:
            if user_id not in data:
                data.append(user_id)
                check = True
        if check:
            self.savedata()
        return check

cubp = cubplugins_permission()