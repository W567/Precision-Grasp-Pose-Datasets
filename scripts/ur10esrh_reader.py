#!/usr/bin/env python
from reader import Reader

class ur10esrhReader(Reader):
  def __init__(self):
    self.robot = "ur10esrh"
    super().__init__()

  def qpos_sort(self, data):
    return " ".join(str(j) for j in data[0:8]) + ' ' + \
           " ".join(str(j) for j in data[13:17][::-1]) + ' ' + \
           " ".join(str(j) for j in data[17:21][::-1]) + ' ' + \
           " ".join(str(j) for j in data[21:25][::-1]) + ' ' + \
           " ".join(str(j) for j in data[25:30][::-1]) + ' ' + \
           " ".join(str(j) for j in data[8:13][::-1])

  def ctrl_sort(self, data):
    return " ".join(str(j) for j in data[0:8]) + ' ' + \
           " ".join(str(j) for j in data[15:17][::-1]) + ' ' + str(data[14] + data[13]) + ' ' + \
           " ".join(str(j) for j in data[19:21][::-1]) + ' ' + str(data[18] + data[17]) + ' ' + \
           " ".join(str(j) for j in data[23:25][::-1]) + ' ' + str(data[22] + data[21]) + ' ' + \
           " ".join(str(j) for j in data[27:30][::-1]) + ' ' + str(data[26] + data[25]) + ' ' + \
           " ".join(str(j) for j in data[8:13][::-1])

read = ur10esrhReader()
read.exe()
