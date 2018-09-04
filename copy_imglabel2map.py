import os
from shutil import copyfile

ROOT_PATH = os.path.split(os.getcwd())[0]
DATASET_PATH = os.path.join(ROOT_PATH, 'BDD')
IMAGES_PATH = os.path.join(DATASET_PATH, 'day_night_separate/images')
LABELS_PATH = os.path.join(DATASET_PATH, 'bdd100k/labels/100k')

# copy val file
val_day_file = os.path.join(DATASET_PATH, 'person_val_day_city_street3000.txt')
val_night_file = os.path.join(DATASET_PATH, 'person_val_night_city_street3000.txt')

# mAP path
MAP_PATH = os.path.join(ROOT_PATH, 'mAP_person')
MAP_IMAGES_PATH = os.path.join(MAP_PATH, 'images/')
MAP_LABELS_PATH = os.path.join(MAP_PATH, 'ground-truth/')

count = 0
with open(val_day_file) as f:
    lines = f.readlines()
    for line in lines:
        image_path = line.split()[0]
        img_name = image_path.split('/')[-1]
        label_path = image_path.replace('/day_night_separate/images/val/day_city_street3000', '/bdd100k/labels/100k/val_bdd2mAP').replace('.jpg', '.txt')
        label_name = label_path.split('/')[-1]
        copyfile(image_path, MAP_IMAGES_PATH + img_name)
        copyfile(label_path, MAP_LABELS_PATH + label_name)
        count += 1
        print(MAP_IMAGES_PATH + img_name)
    print('{} files'.format(count))

count = 0
with open(val_night_file) as f:
    lines = f.readlines()
    for line in lines:
        image_path = line.split()[0]
        img_name = image_path.split('/')[-1]
        label_path = image_path.replace('/day_night_separate/images/val/night_city_street3000', '/bdd100k/labels/100k/val_bdd2mAP').replace('.jpg', '.txt')
        label_name = label_path.split('/')[-1]
        copyfile(image_path, MAP_IMAGES_PATH + img_name)
        copyfile(label_path, MAP_LABELS_PATH + label_name)
        count += 1
    print('{} files'.format(count))
