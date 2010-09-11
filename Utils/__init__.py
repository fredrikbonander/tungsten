import inspect

class dictObj(dict):
    def __getattr__(self, attr):
        return self.get(attr, None)
    __setattr__= dict.__setitem__
    __delattr__= dict.__delitem__

def parsePath(path):
    pathList = path.split('/')
    
    if pathList[-1] == '':
        pathList.pop()
   
    if len(pathList) == 0:
        pathList = ['main']
    
    return pathList

def getPageTemplates(module, clazz):
    return [ cls for name, cls in inspect.getmembers(module) if inspect.isclass(cls) and issubclass(cls, clazz) and cls is not clazz ]