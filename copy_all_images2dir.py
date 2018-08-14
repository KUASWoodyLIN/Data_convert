import os
from glob import glob
from shutil import copyfile


DATASET_PATH = os.path.split(os.getcwd())[0]
COPY_PATH = os.path.join(DATASET_PATH, 'cityscapes/trainset/train_extra')  # TODO: change Path
MAP_PATH = os.path.join(DATASET_PATH, 'mAP')
MAP_IMAGES_PATH = os.path.join(MAP_PATH, 'images/')


src_files = glob(COPY_PATH + '/*/*.png')
dst_files = [MAP_IMAGES_PATH + os.path.split(file)[-1] for file in src_files]


for src, dst in zip(src_files, dst_files):
    copyfile(src, dst)
    # print(src)
    # print(dst)
