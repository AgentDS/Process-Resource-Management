#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/5/24 PM3:42
# @Author  : Shiloh Leung
# @Site    : 
# @File    : main.py
# @Software: PyCharm Community Edition

from ProcessResource import ProcessResourceManager as Manager

inName = 'input.txt'
inFile = open(inName)
outName = 'outShell.txt'
outFile = open(outName, 'w')
ShellTXT = [line for line in inFile.readlines()]
inFile.close()
name = ''
prm = Manager.PRM()
priority = -1
unit = -1
#prm.store()
print('init', file=outFile,end=' ')
print('init', end=' ')
for line in ShellTXT:
    commandList = line.strip().split()
    if len(commandList) >= 1:
        command = commandList[0]
        if command != 'lr' and command != 'lp' and command != 'pinfo':
            print('')
            print(commandList)
        if command == 'init':
            prm.store()
            print(prm.pcb[prm.Current_Running].pid, file=outFile,end=' ')
            print(prm.pcb[prm.Current_Running].pid, end=' ')
        elif command == 'cr':
            name = commandList[1]
            priority = int(commandList[2])
            if prm.contain(name) != -1:
                print("error (duplicate name)",file=outFile,end=' ')
                print("error (duplicate name)", end=' ')
            elif priority > 2 or priority <= 0:
                print("error", file=outFile,end=' ')
                print("error", end=' ')
            else:
                prm.create(name, priority)
                print(prm.pcb[prm.Current_Running].pid, file=outFile, end=' ')
                print(prm.pcb[prm.Current_Running].pid, end=' ')
        elif command == 'de':
            name = commandList[1]
            t = prm.contain(name)
            if t == -1:
                print("error (process not existed)",file=outFile,end=' ')
                print("error (process not existed)", end=' ')
            else:
                prm.destroy(t)
                print(prm.pcb[prm.Current_Running].pid, file=outFile, end=' ')
                print(prm.pcb[prm.Current_Running].pid, end=' ')
        elif command == 'req':
            name = commandList[1]
            unit = int(commandList[2])
            if name == "R1" and unit == 1:
                prm.request(0,unit)
                print(prm.pcb[prm.Current_Running].pid, file=outFile, end=' ')
                print(prm.pcb[prm.Current_Running].pid, end=' ')
            elif name == 'R2' and 0 < unit <= 2:
                prm.request(1,unit)
                print(prm.pcb[prm.Current_Running].pid, file=outFile, end=' ')
                print(prm.pcb[prm.Current_Running].pid, end=' ')
            elif name == 'R3' and 0 < unit <= 3:
                prm.request(2,unit)
                print(prm.pcb[prm.Current_Running].pid, file=outFile, end=' ')
                print(prm.pcb[prm.Current_Running].pid, end=' ')
            elif name == 'R4' and 0 < unit <= 4:
                prm.request(3,unit)
                print(prm.pcb[prm.Current_Running].pid, file=outFile, end=' ')
                print(prm.pcb[prm.Current_Running].pid, end=' ')
            else:
                print("error (invalid request)", file=outFile, end=' ')
                print("error (invalid request)", end=' ')
        elif command == 'lr':
            prm.Resource_Listing(outFile)
        elif command == 'lp':
            prm.Process_Listing(outFile)
        elif command == 'pinfo':
            prm.Process_Info(commandList[1:], outFile)
        elif command == 'rel':
            name = commandList[1]
            unit = int(commandList[2])
            if name == 'R1' and unit == 1:
                if prm.pcb[prm.Current_Running].Other_Resource[0].used >= unit:
                    prm.release(0, unit)
                    print(prm.pcb[prm.Current_Running].pid, file=outFile, end=' ')
                    print(prm.pcb[prm.Current_Running].pid, end=' ')
                else:
                    print('error (release exceed R1 units)', file = outFile, end = ' ')
                    print('error (release exceed R1 units)', end=' ')
            elif name == 'R2' and 0 < unit <= 2:
                if prm.pcb[prm.Current_Running].Other_Resource[1].used >= unit:
                    prm.release(1, unit)
                    print(prm.pcb[prm.Current_Running].pid, file=outFile, end=' ')
                    print(prm.pcb[prm.Current_Running].pid, end=' ')
                else:
                    print('error (release exceed R2 units)', file = outFile, end = ' ')
                    print('error (release exceed R2 units)', end=' ')
            elif name == 'R3' and 0 < unit <= 3:
                if prm.pcb[prm.Current_Running].Other_Resource[2].used >= unit:
                    prm.release(2, unit)
                    print(prm.pcb[prm.Current_Running].pid, file=outFile, end=' ')
                    print(prm.pcb[prm.Current_Running].pid, end=' ')
                else:
                    print('error (release exceed R3 units)', file = outFile, end = ' ')
                    print('error (release exceed R3 units)', end=' ')
            elif name == 'R4' and 0 < unit <= 4:
                if prm.pcb[prm.Current_Running].Other_Resource[3].used >= unit:
                    prm.release(3, unit)
                    print(prm.pcb[prm.Current_Running].pid, file=outFile, end=' ')
                    print(prm.pcb[prm.Current_Running].pid, end=' ')
                else:
                    print('error (release exceed R4 units)', file = outFile, end = ' ')
                    print('error (release exceed R4 units)', end=' ')
            else:
                print('error (invalid release)', file=outFile, end=' ')
                print('error (invalid release)', end=' ')
        elif command == 'to':
            prm.Time_Out()
            print(prm.pcb[prm.Current_Running].pid, file=outFile, end=' ')
            print(prm.pcb[prm.Current_Running].pid, end=' ')
        else:
            print('error (else error)', file=outFile, end=' ')
            print('error (else error)', end=' ')
    else:
        print('\nend')

outFile.close()
