import os
import json
from collections import OrderedDict

# TODO: change Scene
train_day = 'day_city_street100'
train_night = 'night_city_street100'
val = 'day_city_street5'          # 'day_city_street5', 'night_city_street5'


ROOT_PATH = os.path.split(os.getcwd())[0]
DATASET_PATH = os.path.join(ROOT_PATH, 'BDD')
TRAIN_PATH = os.path.join(DATASET_PATH, 'day_night_separate/images')
LABELS_PATH = os.path.join(DATASET_PATH, 'bdd100k/labels/100k')
TRAIN_DAY_IMAGES_PATH = os.path.join(TRAIN_PATH, 'train/' + train_day)
TRAIN_DAY_LABELS_PATH = os.path.join(LABELS_PATH, 'train')
TRAIN_NIGHT_IMAGES_PATH = os.path.join(TRAIN_PATH, 'train/' + train_night)
TRAIN_NIGHT_LABELS_PATH = os.path.join(LABELS_PATH, 'train')
SAVE_TRAIN_DAY_LABELS_FILE = os.path.join(DATASET_PATH, 'train_' + train_day + '.txt')
SAVE_TRAIN_NIGHT_LABELS_FILE = os.path.join(DATASET_PATH, 'train_' + train_night + '.txt')

cls = OrderedDict((('traffic light', 0), ('traffic sign', 1), ('bus', 2),
                   ('truck', 3), ('person', 4), ('motor', 5),
                   ('bike', 6), ('rider', 7), ('train', 8), ('car', 9)))


def convert_bdd2yolo(images_file, read_images_path, read_labels_path, save_file):
    total_name = {}
    save_file = open(save_file, 'w')
    labels_file = [image.split('.')[0]+'.json' for image in images_file]
    for img_file, label_file in zip(images_file, labels_file):
        # read json file
        data = json.load(open(read_labels_path + '/' + label_file, 'r'))
        print('File name: {}'.format(label_file))
        txt = os.path.join(read_images_path, img_file)
        for frame in data['frames']:
            for object in frame['objects']:
                if 'box2d' in object:
                    obj_name = object['category']
                    left = int(object['box2d']['x1'])
                    top = int(object['box2d']['y1'])
                    right = int(object['box2d']['x2'])
                    bottom = int(object['box2d']['y2'])
                    class_id = cls[obj_name]
                    txt += (" " + str(left) + ',' + str(top) + ',' + str(right) + ',' + str(bottom) + ',' + str(class_id))
                    if obj_name in total_name.keys():
                        total_name[obj_name] += 1
                    else:
                        total_name[obj_name] = 0
        save_file.write(txt + '\n')
    save_file.close()
    return total_name


if __name__ == "__main__":
    train_day_images = os.listdir(TRAIN_DAY_IMAGES_PATH)
    train_night_images = os.listdir(TRAIN_NIGHT_IMAGES_PATH)
    train_day_total_name = convert_bdd2yolo(train_day_images, TRAIN_DAY_IMAGES_PATH,
                                            TRAIN_DAY_LABELS_PATH, SAVE_TRAIN_DAY_LABELS_FILE)
    train_night_total_name = convert_bdd2yolo(train_night_images, TRAIN_NIGHT_IMAGES_PATH,
                                              TRAIN_NIGHT_LABELS_PATH, SAVE_TRAIN_NIGHT_LABELS_FILE)

    print('========================================================')
    print("Train day set total classes")
    for key in cls.keys():
        print("{:13}\t{}".format(key, train_day_total_name.get(key, 0)))

    print('========================================================')
    print("Train day set total classes")
    for key in cls.keys():
        print("{:13}\t{}".format(key, train_night_total_name.get(key, 0)))
