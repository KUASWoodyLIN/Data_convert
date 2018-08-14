import os
import re

ROOT_PATH = os.getcwd()
DATA_PATH = os.path.split(ROOT_PATH)[0]
# LABELS_PATH = os.path.join(DATA_PATH, '/media/mmslab-1070/3TData/dataset/BDD/bdd100k_predict/labels/val')
LABELS_PATH = os.path.join(DATA_PATH, '/media/mmslab-1070/3TData/dataset/BDD/bdd100k/labels/100k/val_bdd2mAP/')

files = [os.path.join(LABELS_PATH, file) for file in os.listdir(LABELS_PATH)]

objs = {}
for file in files:
    with open(file, 'r') as f:
        lines = f.readlines()
        for line in lines:
            obj = re.split(' [0-9]+', line)[0]
            if obj in objs.keys():
                objs[obj] += 1
            else:
                objs[obj] = 0

            if obj == 'bike':
                print(file)

print(objs)
