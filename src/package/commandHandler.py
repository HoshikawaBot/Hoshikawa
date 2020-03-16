import package.settings as settings

def cutHead(message, commandName):
    return message[len(settings.prefix + commandName)+1:]