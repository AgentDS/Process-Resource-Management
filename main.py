#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/5/24 PM3:42
# @Author  : Shiloh Leung
# @Site    : 
# @File    : main.py
# @Software: PyCharm Community Edition

from OSAssignment1 import ProcessResourceManager as Manager

pcb = Manager.PCB()
prm1 = Manager.PRM()
print(prm1.pcb[0].type)