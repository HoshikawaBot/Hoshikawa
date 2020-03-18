import re
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))) # 상위 경로 import 가능
from package.tagFunctions import TagFunctions
from inspect import getfullargspec

class __Tag__:
    def __init__(self):
        self.tagFunctions = TagFunctions()
        self.finder = re.compile("\{.*?\}")
        self.splicer = re.compile("(?<!;);(?!;)")
        self.functions = {}

        tempFunctions = list(filter(lambda e: "__" not in e, dir(self.tagFunctions)))

        # object dictionary comfortable function call
        for e in tempFunctions:
            self.functions[e] = {
                "function": eval(f"self.tagFunctions.{e}"),
                "argscount": len(getfullargspec(eval(f"self.tagFunctions.{e}"))[0]) - 1 # because it's method,
                # self exists
            }
        
        # print(self.functions)
    
    def filterNone(self, obj):
        """재귀적으로 Falsy Value('', False, None...)를 필터링하는 method"""
        filterFunc = lambda e: e
        if isinstance(obj, list):
            return list(map(self.filterNone, filter(filterFunc, obj)))
        else:
            return obj
    
    def eval(self, context, params=()):
        """
        tag evaluation core method
        context for db stored value
        params for front-end arguments
        """
        print(self.functions)

        result = context
        i = 0

        # front-end arguments->value 치환 엔진
        for param in params:
            i += 1
            result = result.replace("$" + str(i), param)


        res = re.findall(self.finder, result)
        temp = res
        print(temp)
        res = list(map(lambda e: re.split(self.splicer, e[1:-1]), res))
        res = self.filterNone(res)
        cnt = 0

        # eval 코어 파트(replace 베이스)
        for statement in res:
            print(statement)
            if statement[0] in self.functions and len(statement) - 1 == self.functions[statement[0]]["argscount"]:
                result = result.replace(temp[cnt], self.functions[statement[0]]["function"](*statement[1:]), 1)
            else:
                result = result.replace(temp[cnt], "!!! PARSE ERROR !!!", 1)
            cnt += 1
        
        # Tag의 eval 결과 돌려줌
        return result


Tag = __Tag__()
