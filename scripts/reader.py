#!/usr/bin/env python
import h5py
from math import pi
import xml.etree.ElementTree as ET
import argparse
import random
from datetime import datetime

import rospkg
rospack = rospkg.RosPack()

import mujoco as mj
import mujoco_viewer

def parser():
  parser = argparse.ArgumentParser()
  parser.add_argument('--file', type=str, default='', help='hdf5 filename to be read')
  parser.add_argument('--view', type=int, default=0, help='visualize result or not')
  parser.add_argument('--only', type=int, default=1, help='only show one result for each obj (for visualization only)')
  parser.add_argument('--dura', type=int, default=3000, help='number of steps for each visualization')
  return parser

class Reader():
  def __init__(self):
    self.args = parser().parse_args()
    self.pkg_name = 'pgp_datasets'
    if self.args.file == '':
      self.file_address = rospack.get_path(self.pkg_name) + '/data/hdf5/' + self.robot + '.h5'
    else:
      self.file_address = rospack.get_path(self.pkg_name) + '/data/hdf5/' + self.args.file + '.h5'
    self.xml_path = rospack.get_path(self.pkg_name) +  '/data/robot/' + self.robot + '/scene.xml'
    self.obj_path = rospack.get_path(self.pkg_name) +  '/data/object/'
    self.tree = ET.parse(self.xml_path)
    self.root = self.tree.getroot()
    self.only = self.args.only
    self.dura = self.args.dura
    random.seed(datetime.now().timestamp())

  def qpos_sort(self, data):
    return NotImplementedError

  def ctrl_sort(self, data):
    return NotImplementedError

  def view(self):
    model = mj.MjModel.from_xml_path(self.xml_path)
    data = mj.MjData(model)
    mj.mj_resetDataKeyframe(model, data, 0)
    viewer = mujoco_viewer.MujocoViewer(model, data)
    viewer._render_every_frame = False
    for i in range(self.dura):
      mj.mj_step(model, data)
      viewer.render()
    viewer.close()

  def update_data(self, pose, jnt):
    for body in self.root.iter('body'):
      # update object pose
      if body.get('name') == 'object':
        pos  = ' '.join(str(obj_pos) for obj_pos in pose[:3])
        quat = ' '.join(str(obj_pos) for obj_pos in pose[3:])
        body.set('pos', pos)
        body.set('quat', quat)
    # update robot pose
    jnt = jnt * pi / 180.0
    qpos = self.qpos_sort(jnt) + ' ' + pos + ' ' + quat
    ctrl = self.ctrl_sort(jnt)
    for key in self.root.iter('key'):
      if key.get('name') == 'home':
        key.set('qpos', qpos)
        key.set('ctrl', ctrl)
    
    self.tree.write(self.xml_path)

  def view_data(self):
    with h5py.File(self.file_address, 'r') as f:
      # get names of all objects
      obj_names = [name for name in f.keys()]
      for obj_idx, name in enumerate(obj_names):
        for mesh in self.root.iter('mesh'):
          # change object
          if mesh.get('name') == 'obj':
            mesh.set('file', self.obj_path + name + '.obj')
        # get corresponding poses
        group_read = f[obj_names[obj_idx]]
        if self.only:
          pose_size = len(group_read['pose'][:])
          idx = random.randrange(0, pose_size)
          pose = group_read['pose'][idx]
          jnt = group_read['jnt'][idx]
          self.update_data(pose, jnt)
          gws = group_read['gws'][idx]
          print('GWS: %.4f' % gws)
          self.view()
          if input('next? (q to exit): ') == 'q':
            return
        else:
          for idx, pose in enumerate(group_read['pose']):
            jnt = group_read['jnt'][idx]
            self.update_data(pose, jnt)
            gws = group_read['gws'][idx]
            print('GWS: %.4f' % gws)
            self.view()
            if input('next? (q to exit): ') == 'q':
              return
          
  def read_data(self):
    with h5py.File(self.file_address, 'r') as f:
      obj_names = [name for name in f.keys()]
      obj_size = len(obj_names)
      obj_idx = random.randrange(0, obj_size)
      obj_name = obj_names[obj_idx]
      group_read = f[obj_names[obj_idx]]
      pose_size = len(group_read['pose'][:])
      idx = random.randrange(0, pose_size)
      pose = group_read['pose'][idx]
      jnt = group_read['jnt'][idx]

    for mesh in self.root.iter('mesh'):
      if mesh.get('name') == 'obj':
        mesh.set('file', self.obj_path + obj_name + '.obj')

    self.update_data(pose, jnt)

  def exe(self):
    if self.args.view:
      self.view_data()
    else:
      self.read_data()
