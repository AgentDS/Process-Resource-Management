#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/5/24 PM3:16
# @Author  : Shiloh Leung
# @Site    : 
# @File    : ProcessResourceManager.py
# @Software: PyCharm Community Edition



class RCB:
    def __init__(self):
        self.rid = "Ri"
        self.initial = 0
        self.remain = 0
        self.Wait_List = []

class resource:
    def __init__(self):
        self.rid = -1
        self.used = 0
        self.Wait_Request = 0

class PCB:
    def __init__(self):
        self.pid = " "
        self.type = "ready"
        self.id = -1
        self.parent = -1
        self.child = -1
        self.younger = -1
        self.elder = -1
        self.priority = -1
        tmp_resource = []
        for i in range(4):
            tmp_resource.append(resource())
        self.Other_Resource = tmp_resource

class PRM:
    def __init__(self):
        self.R1 = RCB()
        self.R1.rid = "R1"
        self.R1.initial = 1
        self.R1.remain = 1

        self.R2 = RCB()
        self.R2.rid = "R2"
        self.R2.initial = 2
        self.R2.remain = 2

        self.R3 = RCB()
        self.R3.rid = "R3"
        self.R3.initial = 3
        self.R3.remain = 3

        self.R4 = RCB()
        self.R4.rid = "R4"
        self.R4.initial = 4
        self.R4.remain = 4

        self.rl = [[],[],[]]
        self.del_num = -1
        self.Current_Running = None

        tmp_rcb = []
        for i in range(4):
            tmp_rcb.append(RCB())
        self.rcb = tmp_rcb
        self.rcb[0] = self.R1
        self.rcb[1] = self.R2
        self.rcb[2] = self.R3
        self.rcb[3] = self.R4

        tmp_pcb = []
        for i in range(20):
            tmp_pcb.append(PCB())
        self.pcb = tmp_pcb
        for i in range(20):
            self.pcb[i].id = i
        self.pcb[0].pid = 'init'
        self.pcb[0].priority = 0
        self.rl[0].append(0)
        self.Current_Running = 0


    def Scheduler(self):
        if len(self.rl[2]) != 0:
            self.Current_Running = self.rl[2][0]
            self.pcb[self.Current_Running].type = "running"
            return self.rl[2][0]
        elif len(self.rl[1]) != 0:
            self.Current_Running = self.rl[1][0]
            self.pcb[self.Current_Running].type = "running"
            return self.rl[1][0]
        else:
            self.Current_Running = 0
            self.pcb[self.Current_Running].type = "running"
            return 0


    def Time_Out(self):
        p = self.pcb[self.Current_Running].priority
        self.rl[p].remove(self.Current_Running)
        self.pcb[self.Current_Running].type = "ready"
        self.rl[p].append(self.Current_Running)
        self.Scheduler()

    def release2(self, n, unit):
        self.pcb[self.Current_Running].Other_Resource[n].used -= unit
        self.rcb[n].remain += unit
        tmp_pcb = self.rcb[n].Wait_List[0]
        while (tmp_pcb != 0 and
               self.pcb[tmp_pcb].Other_Resource[n].Wait_Request <= self.rcb[n].remain):
            self.rcb[n].remain -= self.pcb[tmp_pcb].Other_Resource[n].Wait_Request
            self.rcb[n].Wait_List.remove(tmp_pcb)
            self.pcb[tmp_pcb].type = "ready"
            self.pcb[tmp_pcb].Other_Resource[n].used += self.pcb[tmp_pcb].Other_Resource[n].Wait_Request
            self.rl[self.pcb[tmp_pcb].priority].append(tmp_pcb)
            if len(self.rcb[n].Wait_List):
                tmp_pcb = self.rcb[n].Wait_List[0]
            else:
                tmp_pcb = 0

    def release(self, n, unit):
        self.release2(n, unit)
        self.Scheduler()

    def request(self, n, unit):
        if self.rcb[n].remain >= unit:
            self.rcb[n].remain -= unit
            self.pcb[self.Current_Running].Other_Resource[n].rid = n
            self.pcb[self.Current_Running].Other_Resource[n].used += unit
        else:
            self.pcb[self.Current_Running].type = "blocked"
            self.pcb[self.Current_Running].Other_Resource[n].Wait_Request += unit
            self.rcb[n].Wait_List.append(self.Current_Running)
            self.rl[self.pcb[self.Current_Running].priority].remove(self.Current_Running)
        self.Scheduler()

    def isequal(self, value):
        return value == self.del_num

    def destroy(self, n):
        for i in range(4):
            if self.pcb[n].Other_Resource[i].used != 0:
                self.release2(i, self.pcb[n].Other_Resource[i].used)
                if self.rcb[i].remain > self.rcb[i].initial:
                    print("error in destroy: delete resources exit initial units")
                self.pcb[n].Other_Resource[i].rid = -1
                self.pcb[n].Other_Resource[i].used = 0
        if self.pcb[n].type == "ready" or self.pcb[n].type == "running":
            p = self.pcb[n].priority
            self.rl[p].remove(n)
        elif self.pcb[n].type == "blocked":
            for i in range(4):
                if n in self.rcb[i].Wait_List:
                    self.rcb[i].Wait_List.remove(n)
        for i in range(20):
            if self.pcb[i].parent == n:
                self.destroy(self.pcb[i].id)
            if self.pcb[i].id == n:
                self.pcb[i].pid = " "
                self.pcb[i].type = "ready"
                self.pcb[i].parent = -1
                self.pcb[i].child = -1
                self.pcb[i].elder = -1
                self.pcb[i].younger = -1
                self.pcb[i].priority = -1
                for j in range(4):
                    self.pcb[i].Other_Resource[j].rid = -1
                    self.pcb[i].Other_Resource[j].used = 0
                    self.pcb[i].Other_Resource[0].Wait_Request = 0
            if self.pcb[i].elder == n:
                self.pcb[i].elder = -1
            if self.pcb[i].younger == n:
                self.pcb[i].younger = -1
        self.Scheduler()

    def contain(self, name):
        for i in range(20):
            if name == self.pcb[i].pid:
                return i
        return -1

    def create(self, name, p):
        for i in range(20):
            if self.pcb[i].pid == " ":
                self.pcb[i].pid = name
                self.pcb[i].priority = p
                self.rl[p].append(self.pcb[i].id)
                self.pcb[i].parent = self.Current_Running
                if self.pcb[self.Current_Running].child == -1:
                    self.pcb[self.Current_Running].child = i
                for j in range(20):
                    if j < i and self.pcb[j].parent == self.pcb[i].parent:
                        if self.pcb[j].younger == -1:
                            self.pcb[j].younger = i
                        self.pcb[i].elder = j
                break
        self.Scheduler()

    def store(self):
        for i in range(20):
            self.pcb[i].pid = " "
            self.pcb[i].type = "ready"
            self.pcb[i].parent = -1
            self.pcb[i].children = -1
            self.pcb[i].elder = -1
            self.pcb[i].younger = -1
            self.pcb[i].priority = -1
            for j in range(4):
                self.pcb[i].Other_Resource[j].rid = -1
                self.pcb[i].Other_Resource[j].used = 0
                self.pcb[i].Other_Resource[j].Wait_Request = 0
        self.Current_Running = 0
        for i in range(4):
            self.rcb[i].initial = i + 1
            self.rcb[i].remain = i + 1
            while len(self.rcb[i].Wait_List) != 0:
                del self.rcb[i].Wait_List[0]
        for i in range(3):
            while len(self.rl[i]) != 0:
                self.rl[i].pop()

    def Resource_Info(self, outFile):
        nameDict = {}
        print('\n=========Current Resource Information=========', file=outFile)
        print('     initial  remain   Wait List',file=outFile)
        print('\n=========Current Resource Information=========')
        print('     initial  remain   Wait List')
        for i in range(20):
            nameDict[i] = self.pcb[i].pid
        for i in range(4):
            print(self.rcb[i].rid + ':', file=outFile, end='  ')
            print(self.rcb[i].rid + ':',end='  ')
            print(self.rcb[i].initial, file=outFile, end='        ')
            print(self.rcb[i].initial,end='        ')
            print(self.rcb[i].remain, file=outFile,end='        ')
            print(self.rcb[i].remain, end='        ')
            if len(self.rcb[i].Wait_List) != 0:
                for process in self.rcb[i].Wait_List:
                    print(nameDict[process], file=outFile,end=';')
                    print(nameDict[process], end=';')

            else:
                print('None Process is Waiting', file=outFile, end='')
                print('None Process is Waiting', end='')
            print('',file=outFile)
            print('')
        print('', file=outFile)
        print('')

    def Process_Info(self, outFile):
        nameDict = {}
        for i in range(20):
            nameDict[i] = self.pcb[i].pid
        print('\n===============================Current Process Information===============================', file=outFile)
        print('\n===============================Current Process Information===============================')
        print('PID      Status     Priority     Parent     FirstChild     ElderBrother    YoungerBrother', file=outFile)
        print('PID      Status     Priority     Parent     FirstChild     ElderBrother    YoungerBrother')
        for i in range(20):
            if self.pcb[i].pid != ' ':
                print(self.pcb[i].pid, file=outFile, end=(9 - len(self.pcb[i].pid)) * ' ')
                print(self.pcb[i].pid, end=(9 - len(self.pcb[i].pid)) * ' ')
                print(self.pcb[i].type, file=outFile, end=(11 - len(self.pcb[i].type)) * ' ')
                print(self.pcb[i].type, end=(11 - len(self.pcb[i].type)) * ' ')
                print(self.pcb[i].priority, file=outFile, end=(13 - len(str(self.pcb[i].priority))) * ' ')
                print(self.pcb[i].priority, end=(13 - len(str(self.pcb[i].priority))) * ' ')
                if self.pcb[i].parent != -1:
                    parentPid = nameDict[self.pcb[i].parent]
                    print(parentPid, file=outFile, end=(11 - len(parentPid)) * ' ')
                    print(parentPid, end=(11 - len(parentPid)) * ' ')
                else:
                    print('None', file=outFile, end=7 * ' ')
                    print('None', end=7 * ' ')
                if self.pcb[i].child != -1:
                    childPid = nameDict[self.pcb[i].child]
                    print(childPid, file=outFile, end=(15 - len(childPid)) * ' ')
                    print(childPid, end=(15 - len(childPid)) * ' ')
                else:
                    print('None', file=outFile, end=11 * ' ')
                    print('None', end=11 * ' ')
                if self.pcb[i].elder != -1:
                    elderPid = nameDict[self.pcb[i].elder]
                    print(elderPid, file=outFile, end=(16 - len(elderPid)) * ' ')
                    print(elderPid, end=(16 - len(elderPid)) * ' ')
                else:
                    print('None', file=outFile, end=12 * ' ')
                    print('None', end=12 * ' ')
                if self.pcb[i].younger != -1:
                    youngerPid = nameDict[self.pcb[i].younger]
                    print(youngerPid, file=outFile, end=' ')
                    print(youngerPid, end=' ')
                else:
                    print('None', file=outFile,end=' ')
                    print('None',end=' ')
                print('', file=outFile)
                print('')
        print('',file=outFile)
        print('')










