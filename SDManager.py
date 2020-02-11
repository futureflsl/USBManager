import psutil
import sys
import os
import time
import subprocess


class USBManager(object):
    def __init__(self):
        self.number_list=['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    def __GetUsbNameFromPsutil(self):
        device_list=[]
        bad_list = []
        device_all = psutil.disk_partitions()
        if device_all==None or len(device_all) == 0:
            return None,None
        # print(device_all)
        for device in device_all:
            if device.mountpoint.find('/media') >=0 :
                device_list.append(device.device)
            else:
                temp = device.device
                if temp[-1] in self.number_list:
                    temp = temp[0:len(temp)-1]
                if temp not in bad_list:
                    bad_list.append(temp)
        result_list = []
        for device in device_list:
            device_temp = device[0:len(device)-1]
            if device_temp in result_list:
                continue
            result_list.append(device_temp)
        # print(result_list)
        return  result_list, bad_list

    def GetUsbName(self):
        result_shell = self.DoShell('ls /dev/sd*')
        result_psutil, result_bad = self.__GetUsbNameFromPsutil()
        for i in result_shell:
            if i in result_bad:
                continue
            if i not in result_psutil:
                result_psutil.append(i)
        return result_psutil

    def DoShell(self, command, print_msg=False):
        p = subprocess.Popen(
            command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output = p.stdout.readlines()
        if print_msg:
            print(output)
        result = []
        for i in output:
            i = i.decode('utf-8')
            i = i.replace('\n','')
            lastchar = i[-1]
            if lastchar in self.number_list:
                continue
            if i not in result:
                result.append(i)
        return result

if __name__ == "__main__":
    usb = USBManager()
    print('final result device list', usb.GetUsbName())