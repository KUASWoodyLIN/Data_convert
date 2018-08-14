import os
from glob import glob
from shutil import copyfile


DATASET_PATH = os.path.split(os.getcwd())[0]
COPY_FILE = os.path.join(DATASET_PATH, 'VOCdevkit/2007_test.txt')  # TODO: change Path
DST_PATH = os.path.join(DATASET_PATH, 'VOCdevkit/test')


with open(COPY_FILE, 'r') as f:
    lines = f.readlines()
    for line in lines:
        src = line.split(' ')[0]
        dst = os.path.split(src)[-1]
        dst = os.path.join(DST_PATH, dst)
        copyfile(src, dst)
