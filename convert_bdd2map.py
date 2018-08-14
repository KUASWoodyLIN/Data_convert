import os
import json


ROOT_PATH = os.path.split(os.getcwd())[0]
LABELS_PATH = os.path.join(ROOT_PATH, 'BDD/day_night_separate/labels')
TRAIN_LABELS_PATH = os.path.join(LABELS_PATH, 'train/day')
VAL_LABELS_PATH = os.path.join(LABELS_PATH, 'val/day')
# TEST_LABELS_PATH = os.path.join(LABELS_PATH, 'test')

SAVE_TRAIN_LABELS_PATH = os.path.join(LABELS_PATH, 'train_bdd2mAP')
SAVE_VAL_LABELS_PATH = os.path.join(LABELS_PATH, 'val_bdd2mAP')
# SAVE_TEST_LABELS_PATH = os.path.join(LABELS_PATH, 'test_bdd2mAP')

if not os.path.exists(SAVE_TRAIN_LABELS_PATH):
    os.mkdir(SAVE_TRAIN_LABELS_PATH)
if not os.path.exists(SAVE_VAL_LABELS_PATH):
    os.mkdir(SAVE_VAL_LABELS_PATH)
# if not os.path.exists(SAVE_TEST_LABELS_PATH):
#     os.mkdir(SAVE_TEST_LABELS_PATH)


def convert_bdd2map(labels_file, read_path, save_path):
    for file in labels_file:
        # write txt file
        tmp_file = open(save_path+'/'+file.split('.')[0]+'.txt', 'w')
        # read json file
        data = json.load(open(read_path+'/'+file, 'r'))
        print('File name: {}'.format(file))
        for frame in data['frames']:
            for object in frame['objects']:
                if 'box2d' in object:
                    obj_name = object['category']
                    left = object['box2d']['x1']
                    top = object['box2d']['y1']
                    right = object['box2d']['x2']
                    bottom = object['box2d']['y2']
                    tmp_file.write(obj_name + " " +
                                   str(left) + " " +
                                   str(top) + " " +
                                   str(right) + " " +
                                   str(bottom) + '\n')
        tmp_file.close()
    print("Conversion completed!")


if __name__ == "__main__":
    train_labels = os.listdir(TRAIN_LABELS_PATH)
    val_labels = os.listdir(VAL_LABELS_PATH)
    # test_labels = os.listdir(TEST_LABELS_PATH)
    convert_bdd2map(train_labels, TRAIN_LABELS_PATH, SAVE_TRAIN_LABELS_PATH)
    # convert_bdd2map(val_labels, VAL_LABELS_PATH, SAVE_VAL_LABELS_PATH)
    # convert_bdd2map(test_labels, TEST_LABELS_PATH, SAVE_TEST_LABELS_PATH)
