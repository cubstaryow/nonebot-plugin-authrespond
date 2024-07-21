from .plugins_data import wdata , rdata ,initdata
conf_name="cubplugins_permission.json"
bashdata={'global':[],'group-global':[]}
initdata(conf_name,bashdata)


class cubplugins_permission:
    cubplugins_P = rdata(conf_name)

    def __init__(self):
        pass
    
    def savedata(self):
        '''保存数据至本地文件
        '''
        wdata(conf_name,self.cubplugins_P)
    
    def checkperm(self , modulename:str , user_id:str ):
        '''
        检查对用户是否阻断响应 True 阻断 False 响应
        '''
        globaldata = self.cubplugins_P.get('global',[])
        #白名单检查，优先级最高
        if user_id in self.cubplugins_P.get("!-"+modulename,[]):
            return False
        #全局拉黑检查
        if user_id in globaldata:
            return True
        #插件响应检查
        data = self.cubplugins_P.get(modulename,[])
        if user_id in data or '0' in data:
            return True
        return False
    
    def checkpermgroup(self , modulename:str , group_id:str ):
        '''
        检查对群组是否阻断响应 True 阻断 False 响应
        '''
        groupdata = self.cubplugins_P.get('group-global',[])
        #白名单检查，优先级最高
        if group_id in self.cubplugins_P.get("!-group-"+modulename,[]):
            return False
        #全局拉黑检查
        if group_id in groupdata:
            return True
        #插件响应检查
        data = self.cubplugins_P.get('group-'+modulename,[])
        if group_id in data:
            return True
        return False
    
    def setperm(self , modulename:str , user_id:str , allow : bool =False):
        '''
        设定权限
        modulename : 插件名称 (组模式则为group-xxxxxx)(白名单为 !-xxxxxxx)
        user_id : 用户id (组模式传入组ID)
        allow : 是否允许响应 (False则将id拉黑)
        '''
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