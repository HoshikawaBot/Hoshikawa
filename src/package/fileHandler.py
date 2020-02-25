import os

def safeMkdir(path):
    if not os.path.exists(path):
        os.mkdir(path)
        return True
    else:
        return False

def dir(path, count=1):
    def dir_iter(__path__, __count__):
        if __count__ == 0:
            return __path__
        else:
            return dir_iter(os.path.dirname(__path__), __count__ - 1)
    
    return dir_iter(os.path.abspath(path), count)

