# Precision-Grasp-Pose-Datasets

This repository includes automatically generated precision grasp pose datasets towards two robot manipulators: 
- ur5e85:   UR5e robot arm + ROBOTIQ 2f-85
- ur10esrh: UR10e robot arm + ShadowHand

## Overview
Structure of this repository is as below:
```
Precision-Grasp-Pose-Datasets
-- data
  -- hdf5   # generated datasets
  -- object # object mesh files
  -- robot  # robot mjcf and scene files 
-- scripts  # scripts for reading or visualization
```

## Prerequisite
- We use mujoco as the simulator, please follow the official instructions [here](https://github.com/deepmind/mujoco#installation) to install mujoco.

- We use mujoco_python_viewer to help with the visulization in mujoco, please follow the instructions [here](https://github.com/rohanpsingh/mujoco-python-viewer#install) to make it work.

- We use HDF5 to store data, please install h5py as [here](https://github.com/h5py/h5py#installation) to enable accessing HDF5 files with python.

## Getting Started
```
mkdir -p catkin_ws/src
cd catkin_ws/src
# clone this repository
catkin build pgp_datasets
source catkin_ws/devel/setup.bash
```
- reading
```
# reading one data from datasets randomly
# data are stored into the corresponding scene.xml file
# robot pose is stored as the keyframe
# please use the 'Load Key' button inside the mujoco simulator to visualize the robot pose

cd Precision-Grasp-Pose-Datasets/scripts
python ur5e85_reader.py --view 0
python ur10esrh_reader.py --view 0
```

- visualization:
```
cd Precision-Grasp-Pose-Datasets/scripts

# visualization on ur5e85, visualizing all the generated robot pose for each object
python ur5e85_reader.py --view 1 --only 0

# visualizing only one randomly selected robot pose for each object
python ur5e85_reader.py --view 1 --only 1

# visualization on ur10esrh, duration for visualization can be changed with --dura
python ur10esrh_reader.py --view 1 --only 1 --dura 1000

# change the file to be read with --file
python ur10esrh_reader.py --file ur10esrh_4fin --view 1 --only 1 --dura 1000
```
