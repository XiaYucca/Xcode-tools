# -*- coding: utf-8 -*-

import os
import shutil
import time
import xml.etree.ElementTree as ET

def traversalDir_FirstDir(path):
    list = []
    if (os.path.exists(path)):
        files = os.listdir(path)
        for file in files:
            m = os.path.join(path,file)
#            print m
            if (os.path.isdir(m)):
#                h = os.path.split(m)
#                print h[1]
#                list.append(h[1])
                list.append(m)
        return list

def xmlParse(path,devices):
    if (os.path.exists(path)):
        pass
    else:
        print path + " path is not exists"
        return False
    if (os.path.isdir(path)):
        return True
    
    tree = ET.parse(path)
    root = tree.getroot()
    dic = root[0]
    for li in dic:
        str1 = li.text
        if str1:
            for device in devices:
                if device in str1:
                    return False
    return True

def removeDir(path):
    if (os.path.exists(path)):
        pass
    else:
        print path + " path is not exists"
        return
    if (os.path.isdir(path)):
#        shutil.rmtree(path)
        path = path.replace("(","\(")
        path = path.replace(")","\)")
        path = path.replace(" ","\ ")
        os.system("rm -r -f "+path)
        print "remove" + path + " success !!!"
    else:
        print "this is file cannot remove"



if __name__ == "__main__":
    homeDir = os.path.expanduser('~')
    print homeDir
    devices = ["com.apple.CoreSimulator.SimDeviceType.iPhone-Xr","com.apple.CoreSimulator.SimDeviceType.iPhone8","com.apple.CoreSimulator.SimDeviceType.iPhone4"]
    
    iOS_DeviceSupport = 12

    print "........."
#    print "now removing CoreSimulator Devices"
#    rootPath = homeDir + "/Library/Developer/CoreSimulator/Devices"
#    dirs =  traversalDir_FirstDir(rootPath)
#    print list
#    if list.count == 0:
#        print "list empty"
#    for tempPath in dirs:
#        tempFile = tempPath + "/device.plist"
#        res = xmlParse(tempFile,devices)
#
#        if res:
#            removeDir(tempPath)
#            time.sleep(0.1)
#
#
#    print "CoreSimulator devices clear success"
    print "........."
    print "now removing DerivedData"
    time.sleep(1)
#    derivedData = homeDir + "/Library/Developer/Xcode/DerivedData"
    derivedData = homeDir + "/Library/Developer/Xcode/DerivedData"
    removeDir(derivedData)

    print "........."
    print "now removing Archives"
    time.sleep(1)
    Archives = homeDir + "/Library/Developer/Xcode/Archives"
    removeDir(Archives)

    print "........."
    print "now removing Products"
    time.sleep(1)
    Products = homeDir + "/Library/Developer/Xcode/Products"
    removeDir(Products)

    print "........."
    print "now removing XCPGDevices"
    time.sleep(1)
    XCPGDevices = homeDir + "/Library/Developer/XCPGDevices"
    removeDir(XCPGDevices)

'''
    print "........."
    print "now removing iOS DeviceSupport"
    deviceSupportPath = homeDir + "/Library/Developer/Xcode/iOS DeviceSupport"
    dirs =  traversalDir_FirstDir(deviceSupportPath)
#    print list
    if list.count == 0:
        print "list empty"
    for tempPath in dirs:
        h = os.path.split(tempPath)
#        print h[1]
        xp = h[1]
        t = xp.split(".", 1)
        if t :
            x = t[0]
            hi = int(x)
#            print hi
            if hi >= iOS_DeviceSupport:
                pass
            else:
                print "remove " + tempPath
                removeDir(tempPath)
                time.sleep(0.5)
'''




