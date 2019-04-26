import re
import numpy as np


def parse_raw_parameters(raw_parameters):
    # 0:()  ; 1:[]   ; 2:{}
    bracket = np.zeros((3,))
    left = '([{'
    right = ')]}'
    pre_list = []
    cur_word = ''
    for c in raw_parameters:
        if c in left:
            index = left.find(c)
            bracket[index] += 1
        elif c in right:
            index = right.find(c)
            bracket[index] -= 1
        else:
            # 只要有一个非零，说明还在括号匹配阶段
            if bracket.any():
                cur_word += c

            # 正常阶段，词可以被逗号分割
            else:
                # 出现了分隔符
                if c == ',':
                    pre_list.append(cur_word)
                    cur_word = ''
                else:
                    cur_word += c

    # 最后扫尾
    pre_list.append(cur_word)
    ans_list = []
    # 对于list中的子表进行后处理 (变量名与对应的格式)
    for i, item in enumerate(pre_list):
        tmp = item.split(':')
        param_name = tmp[0].strip()
        if len(tmp) <= 1:
            param_type = None
        else:
            if tmp[1].find(',') >= 0:
                param_type = tmp[1].split(',')
            else:
                param_type = tmp[1].strip()
        ans_list.append((param_name, param_type))
    return ans_list


pattern_str = r'def\s+(?P<function_name>[a-zA-Z_][a-zA-Z0-9_]*)\s*\((?P<parameters>.*?)\)\s*(?P<return_type>->.*?){0,1}\s*:'
pattern = re.compile(pattern_str)
with open('meta.py') as f:
    txt = f.read().replace('\n', ' ')

iters = pattern.finditer(txt)
for iter in iters:
    function_name = iter.group('function_name')
    raw_parameters = iter.group('parameters')
    parameters = parse_raw_parameters(raw_parameters)
    raw_return_type = iter.group('return_type')
    if raw_return_type is not None:
        return_type=raw_return_type.replace('->','').strip()
    else:
        return_type=None
    print(function_name)
    print(parameters)
    print(return_type)
