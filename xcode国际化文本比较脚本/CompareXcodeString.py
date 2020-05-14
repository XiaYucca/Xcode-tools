# -*- coding: utf-8 -*-

import sys
import getopt
import re
import urllib2
import json
import sys
import urllib
import string
import time

helpDocument = '''
******************************************
     xcode 国际化 文本比较脚本
   比较文本1 中 没有文本2 中的key
   比较文本2 中 没有文本1 中的key
翻译 文本1 中 没有文本2 中的key 对应的英文

-f [需要比较的文件名1] -t [需要比较的文件名2] -c 只支持中文到英文翻译

******************************************
'''

reload(sys)
sys.setdefaultencoding('utf8')

flag = False
convertFlag = False


def Handle_single_comment(lines, i):
    index = lines[i].find("//")
    if index != -1:
        # lines[i] = lines[i][0:index]
        lines[i] = lines[i].replace(lines[i], '', 1)
        lines[i] += ''


def Handle_document_comment(lines, i):
    global flag
    while True:
        if not flag:
            index = lines[i].find("/*")
            if index != -1:
                flag = True
                index2 = lines[i].find("*/", index + 2)
                if index2 != -1:
                    lines[i] = lines[i].replace(lines[i], '', 1)
                    flag = False  # continue look for comment
                else:
                    lines[i] = lines[i].replace(lines[i], '', 1)  # only find "begin comment
                    lines[i] += ''
                    return -2
            else:
                return 0  # not find
        else:
            index2 = lines[i].find("*/")
            if index2 != -1:
                flag = False
                lines[i] = lines[i].replace(lines[i], '', 1)  # continue look for comment
            else:
                return -1  # should delete this
                
def RemoveComment(file):
    global flag
    f = open(file, "r")
    lines = f.readlines()
    f.close()
    length = len(lines)
    i = 0
    while i < length:
        ret = Handle_document_comment(lines, i)
        if ret == -1:
            if flag == False:
                print("There must be some wrong")
            del lines[i]
            i -= 1
            length -= 1
        elif ret == 0:
            Handle_single_comment(lines, i)
        else:
            pass
        i += 1
    return lines
    
def getKeysInStringFile(fileName):
    lines = RemoveComment(fileName)
    linesString = ''.join(lines)
    keyList = []
    keys = linesString.split(";")
    for key in keys:
        ke = key.split("=")
        if len(ke) < 2:
            continue
        k = ke[0]
        ks = re.findall('"(.*)"',k)
        if len(ks) < 1:
            continue
        k = ks[0]
        keyList.append(k)
#        print k
    return keyList


def main(argv):
    global convertFlag ,helpDocument
    try:
#     options, args = getopt.getopt(argv, "hp:i:", ["help", "ip=", "port="])
        options, args = getopt.getopt(argv, "hf:t:c", ["help", "from=","to=","convert"])
    except getopt.GetoptError:
        print(helpDocument)
        sys.exit()
    file1 = None
    file2 = None
    for option, value in options:
        if option in ("-h", "--help"):
            print(helpDocument)
            break
        if option in ("-f", "--from"):
            file1 = value
            continue
        if option in ("-t", "--to"):
            file2 = value
            continue
        if option in ("-c", "--convert"):
            convertFlag = True
            continue
    if file1 is None :
        print("错误：文件为空 详细 使用--help")
        return
    if file2 is None:
        print("错误：文件为空 详细 使用--help")
        return
    compareFile(file1,file2)
    
        
def compareFile(fileName1,fileName2):
    
    enKeys = getKeysInStringFile(fileName1)
    spKeys = getKeysInStringFile(fileName2)
    
    file1 = fileName1.split("/")[-1]
    file2 = fileName2.split("/")[-1]

    print "##################" + file1 + "中存在" + file2 + "中不存在#####################"
    defkey = set(enKeys) - set(spKeys)
    for key in defkey:
        print key
    print "#############################################################################\r\n\r\n"

    print "##################" + file2 + "中存在" + file1 + "中不存在#####################"
    defkey2 = set(spKeys) - set(enKeys)
    for key in defkey:
        print key
    print "############################################################################\r\n\r\n"
    
    if convertFlag:
        tranLines(defkey2,"ZH_CN2EN")
    
    
def tranLines(lines,language):
    print "##################有道正在翻译 中文-》英文#####################"
    for line in lines:
        newValue = trans(language,line)
        str = '"' + line + '" = "' + newValue + '";'
        print str
        time.sleep(0.5)
    

def trans(code,source):
#    http://fanyi.youdao.com/translate?&doctype=json&type=ZH_CN2EN&i=你好
    url = 'http://fanyi.youdao.com/translate?&doctype=json&type='+code+'&i=' + source
#    url = 'http://translate.google.cn/translate_a/single?client=gtx&dt=t&dj=1&ie=UTF-8&sl=auto&tl='+ code + '&q=' + source

    url = urllib.quote(str(url), safe=string.printable)
    rq = urllib2.Request(url.encode('utf-8'))
    try:
        rs = urllib2.urlopen(rq).read()
        #urllib2.urlopen(rq).read()
        dict = json_to_dict(rs)
        res = resultFromJson(dict)
        return res
    except:
        return ""
        
def dict_to_json(dict):
#    j = json.dumps(dict)
    j =json.dumps(dict, ensure_ascii=False, encoding='UTF-8')
    return j

def json_to_dict(j):
    dict = json.loads(s=j)
#    print(dict)
    return dict

def resultFromJson(j):
    resDic = j["translateResult"]
    resArr = resDic[0]
    resArr = resArr[0]
    resStr = resArr["tgt"]
    return resStr
        
if __name__ == '__main__':
    main(sys.argv[1:])

