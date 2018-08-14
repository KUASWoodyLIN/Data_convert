import os
import cv2
import math
import numpy as np
import matplotlib.pyplot as plt

objects_count = {}

# opencv draw
def draw_yolo_bboxes(lines, labels, save_path=False):
    for line in lines:
        tmp = line.split()
        img = tmp[0]
        boxes = tmp[1:]
        file_name = os.path.split(img)[-1]
        img = cv2.imread(img)
        for box in boxes:
            box = box.split(',')
            xmin = int(box[0])
            ymin = int(box[1])
            xmax = int(box[2])
            ymax = int(box[3])
            label_name = labels[int(box[4])]
            crop_img = img[ymin-5:ymax+5, xmin-5:xmax+5]
            objects_count[label_name] = objects_count.setdefault(label_name, 0) + 1
            if save_path:
                output_img_path = save_path + '/' + label_name + '/' + str(objects_count[label_name]) + '.jpg'
                print(output_img_path)
                cv2.imwrite(output_img_path, crop_img)
            else:
                cv2.imshow('show', crop_img)
                k = cv2.waitKey(1)
                if k == 27:
                    break
    if not save_path:
        cv2.destroyAllWindows()


if __name__ == '__main__':
    ROOT_PATH = os.path.split(os.getcwd())[0]
    DATASET_PATH = os.path.join(ROOT_PATH, 'BDD')
    # BDD Dataset
    bdd_labels = ['traffic light', 'traffic sign', 'bus', 'truck', 'person', 'motor', 'bike', 'rider', 'train', 'car']
    SAVE_IMAGES = True      # TODO: You can change True or False
    DATASET_NAME = 'val_night.txt'    # TODO: You can change <train, val, train_day, train_night, val_day, val_night>
    input_file = os.path.join(DATASET_PATH, DATASET_NAME)

    with open(input_file) as f:
        lines = f.readlines()
    if SAVE_IMAGES:
        save_path = os.path.join(DATASET_PATH, 'bdd100k/night_images_crop')
        if not os.path.exists(save_path):
            for i in bdd_labels:
                os.makedirs(os.path.join(save_path, i))
        draw_yolo_bboxes(lines, bdd_labels, save_path)
    else:
        draw_yolo_bboxes(lines, bdd_labels)

    print('========================================================')
    print("Validation set total classes")
    for key in bdd_labels:
        print("{:13}\t{}".format(key, objects_count.get(key, 0)))

