import os
import json
import cv2
from collections import OrderedDict

ROOT_PATH = os.path.split(os.getcwd())[0]
DATASET_PATH = os.path.join(ROOT_PATH, 'BDD')
ATTRUBUTES_PATH = os.path.join(DATASET_PATH, 'attributes')
TRAIN_PATH = os.path.join(DATASET_PATH, 'bdd100k/images/100k')
LABELS_PATH = os.path.join(DATASET_PATH, 'bdd100k/labels/100k')
TRAIN_IMAGES_PATH = os.path.join(TRAIN_PATH, 'train')
TRAIN_LABELS_PATH = os.path.join(LABELS_PATH, 'train')
VAL_IMAGES_PATH = os.path.join(TRAIN_PATH, 'val')
VAL_LABELS_PATH = os.path.join(LABELS_PATH, 'val')

if not os.path.exists(ATTRUBUTES_PATH):
    os.mkdir(ATTRUBUTES_PATH)


def show_classes(labels_file, read_labels_path, read_images_path):
    dataset = os.path.split(read_images_path)[-1]
    weather = {}
    weather_img = {}
    scene = {}
    scene_img = {}
    timeofday = {}
    timeofday_img = {}
    cls = OrderedDict((('traffic light', 0), ('traffic sign', 0), ('bus', 0),
                       ('truck', 0), ('person', 0), ('motor', 0),
                       ('bike', 0), ('rider', 0), ('train', 0), ('car', 0)))
    for file in labels_file:
        data = json.load(open(read_labels_path + '/' + file, 'r'))
        attributes = data['attributes']
        img_file = read_images_path + '/' + file.split('.')[0] + '.jpg'
        if attributes['weather'] in weather.keys():
            weather[attributes['weather']] += 1
            weather_img[attributes['weather']].append(img_file)
        else:
            weather[attributes['weather']] = 1
            weather_img[attributes['weather']] = [img_file]

        if attributes['scene'] in scene.keys():
            scene[attributes['scene']] += 1
            scene_img[attributes['scene']].append(img_file)
        else:
            scene[attributes['scene']] = 1
            scene_img[attributes['scene']] = [img_file]

        if attributes['timeofday'] in timeofday.keys():
            timeofday[attributes['timeofday']] += 1
            timeofday_img[attributes['timeofday']].append(img_file)
        else:
            timeofday[attributes['timeofday']] = 1
            timeofday_img[attributes['timeofday']] = [img_file]

        for frame in data['frames']:
            for object in frame['objects']:
                if 'box2d' in object:
                    cls[object['category']] += 1

    classes_file = open(os.path.join(DATASET_PATH, dataset+'_classes'), 'w')
    print('--------------------------------------------------------')
    classes_file.write('--------------------------------------------------------\n')
    for key, value in weather.items():
        print("{:13}\t{}".format(key, value))
        classes_file.write("{:13}\t{}\n".format(key, value))

    print('--------------------------------------------------------')
    classes_file.write('--------------------------------------------------------\n')

    for key, value in scene.items():
        print("{:13}\t{}".format(key, value))
        classes_file.write("{:13}\t{}\n".format(key, value))

    print('--------------------------------------------------------')
    classes_file.write('--------------------------------------------------------\n')
    for key, value in timeofday.items():
        print("{:13}\t{}".format(key, value))
        classes_file.write("{:13}\t{}\n".format(key, value))

    print('--------------------------------------------------------')
    classes_file.write('--------------------------------------------------------\n')
    for key, value in cls.items():
        print("{:13}\t{}".format(key, value))
        classes_file.write("{:13}\t{}\n".format(key, value))
    classes_file.close()

    for key in weather_img.keys():
        with open(os.path.join(ATTRUBUTES_PATH, dataset+'_weather_' + key + '.txt'), 'w') as f:
            for file in weather_img[key]:
                f.write(file+'\n')

    for key in scene_img.keys():
        with open(os.path.join(ATTRUBUTES_PATH, dataset+'_scene_' + key + '.txt'), 'w') as f:
            for file in scene_img[key]:
                f.write(file+'\n')

    timeofday_img['dawndusk'] = timeofday_img['dawn/dusk']
    del timeofday_img['dawn/dusk']
    for key in timeofday_img.keys():
        with open(os.path.join(ATTRUBUTES_PATH, dataset+'_timeofday_' + key + '.txt'), 'w') as f:
            for file in timeofday_img[key]:
                f.write(file+'\n')


def show_image(file):
    data = open(file, 'r')
    imgs_file = data.readlines()
    for img_file in imgs_file:
        img_file = img_file.split('\n')[0]
        img = cv2.imread(img_file)
        cv2.imshow('image', img)
        k = cv2.waitKey(0)
        if k == 27:
            print('Finish')
            break
    cv2.destroyAllWindows()



if __name__ == '__main__':

    train_labels = os.listdir(TRAIN_LABELS_PATH)
    val_labels = os.listdir(VAL_LABELS_PATH)

    print('========================================================')
    print("Train set total classes")
    show_classes(train_labels, TRAIN_LABELS_PATH, TRAIN_IMAGES_PATH)
    
    print('========================================================')
    print("validation set total classes")
    show_classes(val_labels, VAL_LABELS_PATH, VAL_IMAGES_PATH)

    # print('========================================================')
    # attributes_file = '/home/woodylin/dataset/BDD/attributes/' + 'val_timeofday_undefined.txt'
    # attributes_file = '/home/woodylin/dataset/BDD/attributes/' + 'val_weather_rainy.txt'
    # attributes_file = '/home/woodylin/dataset/BDD/attributes/' + 'val_scene_tunnel.txt'

    # show_image(attributes_file)




