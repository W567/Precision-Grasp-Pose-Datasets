#!/usr/bin/env python
from reader import Reader
import numpy as np

class ur5e85Reader(Reader):
  def __init__(self):
    self.ext = np.array([1, 1, 1, -1, 1, 1, 1, -1])
    self.robot = "ur5e85"
    super().__init__()

  def qpos_sort(self, data):
    hand_qpos = self.ext * data[-1]
    return " ".join(str(j) for j in data[0:6]) + ' ' + \
           " ".join(str(j) for j in hand_qpos[:])

  def ctrl_sort(self, data):
    return " ".join(str(j) for j in data[0:6]) + ' ' + str(data[6] * 255 / 0.8)

read = ur5e85Reader()
read.exe()
