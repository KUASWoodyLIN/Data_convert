import os
import json
from collections import OrderedDict


ROOT_PATH = os.path.split(os.getcwd())[0]
DATASET_PATH = os.path.join(ROOT_PATH, 'BDD')
TRAIN_PATH = os.path.join(DATASET_PATH, 'bdd100k/images/100k')
LABELS_PATH = os.path.join(DATASET_PATH, 'bdd100k/labels/100k')
TRAIN_IMAGES_PATH = os.path.join(TRAIN_PATH, 'train')
TRAIN_LABELS_PATH = os.path.join(LABELS_PATH, 'train')
VAL_IMAGES_PATH = os.path.join(TRAIN_PATH, 'val')
VAL_LABELS_PATH = os.path.join(LABELS_PATH, 'val')

SAVE_TRAIN_LABELS_FILE = os.path.join(DATASET_PATH, 'train.txt')
SAVE_VAL_LABELS_FILE = os.path.join(DATASET_PATH, 'val.txt')


cls = OrderedDict((('traffic light', 0), ('traffic sign', 1), ('bus', 2),
                   ('truck', 3), ('person', 4), ('motor', 5),
                   ('bike', 6), ('rider', 7), ('train', 8), ('car', 9)))


def convert_bdd2yolo(labels_file, read_images_path, read_labels_path, save_file):
    total_name = {}
    save_file = open(save_file, 'w')
    for file in labels_file:
        # read json file
        data = json.load(open(read_labels_path + '/' + file, 'r'))
        print('File name: {}'.format(file))
        txt = os.path.join(read_images_path, file.split('.')[0]+'.jpg')
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
    train_labels = os.listdir(TRAIN_LABELS_PATH)
    val_labels = os.listdir(VAL_LABELS_PATH)
    train_total_name = convert_bdd2yolo(train_labels, TRAIN_IMAGES_PATH, TRAIN_LABELS_PATH, SAVE_TRAIN_LABELS_FILE)
    val_total_name = convert_bdd2yolo(val_labels, VAL_IMAGES_PATH, VAL_LABELS_PATH, SAVE_VAL_LABELS_FILE)

    print('========================================================')
    print("Train set total classes")
    for key in cls.keys():
        print("{:13}\t{}".format(key, train_total_name[key]))

    print('========================================================')
    print("validation set total classes")
    for key in cls.keys():
        print("{:13}\t{}".format(key, val_total_name[key]))
