import os
import cv2
import math
import numpy as np
import matplotlib.pyplot as plt


# opencv draw
def draw_yolo_bboxes(input_file, labels, save_path=False):
    colors = np.array(plt.cm.hsv(np.linspace(0, 1, 21)).tolist()) * 255
    # cv2.applyColorMap(np.arange(21), color, cv2.COLORMAP_HSV)
    with open(input_file) as f:
        lines = f.readlines()
        for line in lines:
            tmp = line.split(" ")
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
                label = int(box[4])
                color = colors[label]
                cv2.rectangle(img, (xmin, ymin), (xmax, ymax), color, 1)
                font_size = math.sqrt((xmax - xmin) * (ymax - ymin)) / 50
                if font_size > 1:
                    font_size = 1
                elif font_size < 0.3:
                    font_size = 0.3
                cv2.putText(img,
                            labels[label],
                            (xmin, ymin - 2),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            font_size,
                            color, 1)
            if save_path:
                output_img_path = os.path.join(save_path, file_name)
                print(output_img_path)
                cv2.imwrite(output_img_path, img)
            else:
                cv2.imshow('show', img)
                k = cv2.waitKey(0)
                if k == 27:
                    break
    if not save_path:
        cv2.destroyAllWindows()


if __name__ == '__main__':
    DATASET_PATH = os.path.split(os.getcwd())[0]

    # Cityscapes Dataset
    # input_file = os.path.join(DATASET_PATH, 'cityscapes/trainset/train_extra_day.txt')
    # cs_labels = ['person',  'rider',  'car', 'truck', 'bus', 'motorcycle', 'bicycle', 'caravan',
    #              'trailer', 'traffic sign', 'traffic light']
    # draw_yolo_bboxes(input_file, bdd_labels)

    # BDD Dataset
    # Do you want to save bboxes images?
    SAVE_IMAGES = True      # TODO: You can change True or False
    DATASET_NAME = 'val'    # TODO: You can change <train, val, train_day, train_night, val_day, val_night>
    bdd_labels = ['traffic light', 'traffic sign', 'bus', 'truck', 'person', 'motor', 'bike', 'rider', 'train', 'car']

    input_file = os.path.join(DATASET_PATH, 'BDD/' + DATASET_NAME + '.txt')
    if SAVE_IMAGES:
        save_path = os.path.join(DATASET_PATH, 'BDD/bdd100k/images_with_bboxes/' + DATASET_NAME)
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        draw_yolo_bboxes(input_file, bdd_labels, save_path)
    else:
        draw_yolo_bboxes(input_file, bdd_labels)


    # VOC Dataset
    # input_file = os.path.join(DATASET_PATH, 'VOCdevkit/2007_train.txt')
    # voc_labels = ['aeroplane', 'bicycle', 'bird', 'boat', 'bottle', 'bus', 'car', 'cat',
    #               'chair', 'cow', 'diningtable', 'dog', 'horse', 'motorbike', 'person',
    #               'pottedplant', 'sheep', 'sofa', 'train', 'tvmonitor']
    # draw_yolo_bboxes(input_file, voc_labels)
