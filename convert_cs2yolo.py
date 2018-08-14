import os
import json
import random
from collections import OrderedDict
from glob import glob

ROOT_PATH = os.getcwd()
DATA_PATH = os.path.split(ROOT_PATH)[0]
CS_DATASET = os.path.join(DATA_PATH, 'cityscapes')
ANNOTATION_PATH = os.path.join(CS_DATASET, 'gtCoarse/train_extra')

files = glob(ANNOTATION_PATH+'/*/*.json')
cls = OrderedDict((('person', 0), ('rider', 1), ('car', 2),
                   ('truck', 3), ('bus', 4), ('motorcycle', 5),
                   ('bicycle', 6), ('caravan', 7), ('trailer', 8),
                   ('traffic sign', 9), ('traffic light', 10)))


def convert_cs2yolo(trainset):
    dataset_choose = []
    images_path = []
    for i in range(trainset['day']):
        dataset_choose.append(0)
        images_path.append('trainset/train_extra')
    for i in range(trainset['dark']):
        dataset_choose.append(0)
        images_path.append('trainset/train_extra_dark')
    for i in range(trainset['darker']):
        dataset_choose.append(0)
        images_path.append('trainset/train_extra_darker')

    if len(images_path) == 1:
        save_file = os.path.join(CS_DATASET, 'trainset/train_extra_day.txt')
        day_night = False
    else:
        save_file = os.path.join(CS_DATASET, 'trainset/train_extra_random.txt')
        day_night = True

    save_file = open(save_file, 'w')
    total_name = {}
    no_obj_file = 0
    for file in files:
        data = json.load(open(file, 'r'))
        print('File name: {}'.format(os.path.split(file)[-1]))
        if day_night:
            i = random.randint(0, len(images_path)-1)
            dataset_choose[i] += 1
            image_file = images_path[i].join(file.split('gtCoarse_polygons.json')[0].split('gtCoarse/train_extra')) \
                         + 'leftImg8bit.png'
        else:
            image_file = images_path[0].join(file.split('gtCoarse_polygons.json')[0].split('gtCoarse/train_extra')) \
                         + 'leftImg8bit.png'
        txt = image_file
        no_obj = [True]
        for obj in data['objects']:
            obj_name = obj['label']
            if obj_name in cls:
                ploy = obj['polygon']
                # TODO: bboxes
                xs, ys = [], []
                for x, y in ploy:
                    xs.append(x)
                    ys.append(y)
                left = min(xs)
                top = min(ys)
                right = max(xs)
                bottom = max(ys)
                class_id = cls[obj_name]
                txt += (" " + str(left) + ',' + str(top) + ',' + str(right) + ',' + str(bottom) + ',' + str(class_id))
                no_obj = False
            if obj_name in total_name.keys():
                total_name[obj_name] += 1
            else:
                total_name[obj_name] = 0

        if no_obj:
            no_obj_file += 1
            dataset_choose[i] -= 1
            print("ERROR no object file".format(file))
        else:
            save_file.write(txt + '\n')
    save_file.close()
    print("Day {}, dark {}, darker{}".format(dataset_choose[0] + dataset_choose[1], dataset_choose[2], dataset_choose[3]))
    print("Total {} files no object".format(no_obj_file))
    print(total_name)
    print('=============================================================')
    for key in cls.keys():
        print("{:13}\t{}".format(key, total_name[key]))


if __name__ == '__main__':
    # Here you can Change the scale between <day, dark, darker> three type of datasets
    trainset = {'day': 1, 'dark': 0, 'darker': 0}
    convert_cs2yolo(trainset)
