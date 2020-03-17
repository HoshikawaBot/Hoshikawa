import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))) # 상위 경로 import 가능
import package.settings as settings

def cutHead(message, commandName):
    return message[len(settings.prefix + commandName)+1:]