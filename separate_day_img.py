import os
from shutil import copyfile
import argparse

parser = argparse.ArgumentParser(description='Separate the different scenes images.')

# Models Setting
parser.add_argument('--separate_dir', type=str, help='Create the separate dir name', default='day_night_separate')
parser.add_argument('--separate_type', type=str, help='day/night/cloudy/rainy/...', default='night')


ROOT_PATH = os.path.split(os.getcwd())[0]
DATASET_PATH = os.path.join(ROOT_PATH, 'BDD')


def separate(train_files, val_file, separate_dir, scenes_type):
    images_train_dir = os.path.join(separate_dir, 'images/train')
    images_val_dir = os.path.join(separate_dir, 'images/val')
    labels_train_dir = os.path.join(separate_dir, 'labels/train')
    labels_val_dir = os.path.join(separate_dir, 'labels/val')

    images_train_dir_type = os.path.join(images_train_dir, scenes_type)
    images_val_dir_type = os.path.join(images_val_dir, scenes_type)
    labels_train_dir_type = os.path.join(labels_train_dir, scenes_type)
    labels_val_dir_type = os.path.join(labels_val_dir, scenes_type)

    os.makedirs(images_train_dir_type)
    os.makedirs(images_val_dir_type)
    os.makedirs(labels_train_dir_type)
    os.makedirs(labels_val_dir_type)

    data = open(train_files, 'r')
    lines = data.readlines()
    for line in lines:
        images_src = line.split('\n')[0]
        images_dst = os.path.split(line)[-1].split('\n')[0]
        print(images_dst)
        images_dst = os.path.join(images_train_dir_type, images_dst)
        copyfile(images_src, images_dst)
        labels_src = images_src.replace('images', 'labels').replace('.jpg', '.json')
        labels_dst = images_dst.replace('images', 'labels').replace('.jpg', '.json')
        copyfile(labels_src, labels_dst)

    data = open(val_file, 'r')
    lines = data.readlines()
    for line in lines:
        images_src = line.split('\n')[0]
        images_dst = os.path.split(line)[-1].split('\n')[0]
        print(images_dst)
        images_dst = os.path.join(images_val_dir_type, images_dst)
        copyfile(images_src, images_dst)
        labels_src = images_src.replace('images', 'labels').replace('.jpg', '.json')
        labels_dst = images_dst.replace('images', 'labels').replace('.jpg', '.json')
        copyfile(labels_src, labels_dst)


if __name__ == '__main__':
    args = parser.parse_args()
    SEPARATE_DIR = os.path.join(DATASET_PATH, args.separate_dir)
    scenes_type = args.separate_type

    train_file = os.path.join(DATASET_PATH, 'attributes/train_timeofday_night.txt')
    val_file = os.path.join(DATASET_PATH, 'attributes/val_timeofday_night.txt')
    separate(train_file, val_file, SEPARATE_DIR, scenes_type)

    # train_file = os.path.join(DATASET_PATH, 'attributes/train_timeofday_night.txt')
    # val_file = os.path.join(DATASET_PATH, 'attributes/val_timeofday_night.txt')
    # separate(train_file, val_file, SEPARATE_DIR, scenes_type)

