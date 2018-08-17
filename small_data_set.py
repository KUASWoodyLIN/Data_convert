import os
import shutil
import numpy as np


# setting
Numbers_train = 3000
Numbers_val = 3000
Scene = 'city_street'  # or 'residential.txt'

ROOT_PATH = os.path.split(os.getcwd())[0]
DATASET_PATH = os.path.join(ROOT_PATH, 'BDD')

# SAVE PATH
TRAIN_DAY_IMAGES_PATH = os.path.join(DATASET_PATH, 'day_night_separate/images/train/day_' + Scene + str(Numbers_train))
TRAIN_DAY_LABELS_PATH = os.path.join(DATASET_PATH, 'day_night_separate/labels/train/day_' + Scene + str(Numbers_train))
TRAIN_NIGHT_IMAGES_PATH = os.path.join(DATASET_PATH, 'day_night_separate/images/train/night_' + Scene + str(Numbers_train))
TRAIN_NIGHT_LABELS_PATH = os.path.join(DATASET_PATH, 'day_night_separate/labels/train/night_' + Scene + str(Numbers_train))
VAL_DAY_IMAGES_PATH = os.path.join(DATASET_PATH, 'day_night_separate/images/val/day_' + Scene + str(Numbers_val))
VAL_DAY_LABELS_PATH = os.path.join(DATASET_PATH, 'day_night_separate/labels/val/day_' + Scene + str(Numbers_val))
VAL_NIGHT_IMAGES_PATH = os.path.join(DATASET_PATH, 'day_night_separate/images/val/night_' + Scene + str(Numbers_val))
VAL_NIGHT_LABELS_PATH = os.path.join(DATASET_PATH, 'day_night_separate/labels/val/night_' + Scene + str(Numbers_val))

# Attributes
TRAIN_DAY = os.path.join(DATASET_PATH, 'attributes/train_timeofday_daytime.txt')
TRAIN_NIGHT = os.path.join(DATASET_PATH, 'attributes/train_timeofday_night.txt')
TRAIN_SCENE = os.path.join(DATASET_PATH, 'attributes/train_scene_' + Scene + '.txt')
VAL_DAY = os.path.join(DATASET_PATH, 'attributes/val_timeofday_daytime.txt')
VAL_NIGHT = os.path.join(DATASET_PATH, 'attributes/val_timeofday_night.txt')
VAL_SCENE = os.path.join(DATASET_PATH, 'attributes/val_scene_' + Scene + '.txt')
# Weather Attributes
TRAIN_WEATHER_CLEAR = os.path.join(DATASET_PATH, 'attributes/train_weather_clear.txt')
TRAIN_WEATHER_OVERCAST = os.path.join(DATASET_PATH, 'attributes/train_weather_overcast.txt')
TRAIN_WEATHER_CLOUDY = os.path.join(DATASET_PATH, 'attributes/train_weather_partly cloudy.txt')
VAL_WEATHER_CLEAR = os.path.join(DATASET_PATH, 'attributes/val_weather_clear.txt')
VAL_WEATHER_OVERCAST = os.path.join(DATASET_PATH, 'attributes/val_weather_overcast.txt')
VAL_WEATHER_CLOUDY = os.path.join(DATASET_PATH, 'attributes/val_weather_partly cloudy.txt')

# clear, overcast, partly cloudy

# read images list
train_day_images = set([path.split('\n')[0] for path in open(TRAIN_DAY, 'r').readlines()])
train_night_images = set([path.split('\n')[0] for path in open(TRAIN_NIGHT, 'r').readlines()])
train_scene_images = set([path.split('\n')[0] for path in open(TRAIN_SCENE, 'r').readlines()])
val_day_images = set([path.split('\n')[0] for path in open(VAL_DAY, 'r').readlines()])
val_night_images = set([path.split('\n')[0] for path in open(VAL_NIGHT, 'r').readlines()])
val_scene_images = set([path.split('\n')[0] for path in open(VAL_SCENE, 'r').readlines()])
# read weather images list
train_weather_clear_images = [path.split('\n')[0] for path in open(TRAIN_WEATHER_CLEAR, 'r').readlines()]
train_weather_overcast_images = [path.split('\n')[0] for path in open(TRAIN_WEATHER_OVERCAST, 'r').readlines()]
train_weather_cloudy_images = [path.split('\n')[0] for path in open(TRAIN_WEATHER_CLOUDY, 'r').readlines()]
val_weather_clear_images = [path.split('\n')[0] for path in open(VAL_WEATHER_CLEAR, 'r').readlines()]
val_weather_overcast_images = [path.split('\n')[0] for path in open(VAL_WEATHER_OVERCAST, 'r').readlines()]
val_weather_cloudy_images = [path.split('\n')[0] for path in open(VAL_WEATHER_CLOUDY, 'r').readlines()]
train_weather = set(train_weather_clear_images + train_weather_overcast_images + train_weather_cloudy_images)
val_weather = set(val_weather_clear_images + val_weather_overcast_images + val_weather_cloudy_images)

# get day, night and town intersection
train_scene_day = list(train_day_images.intersection(train_scene_images, train_weather))
train_scene_night = list(train_night_images.intersection(train_scene_images, train_weather))
val_scene_day = list(val_day_images.intersection(val_scene_images, val_weather))
val_scene_night = list(val_night_images.intersection(val_scene_images, val_weather))


def copy_samples(copy_images, copy_images_path_dst, copy_labels_path_dst, number):
    copy_images.sort()
    # Create images path
    if os.path.exists(copy_images_path_dst):   # if it exist already
      shutil.rmtree(copy_images_path_dst)
    if not os.path.exists(copy_images_path_dst):
        os.makedirs(copy_images_path_dst)
    # Create labels path
    if os.path.exists(copy_labels_path_dst):   # if it exist already
      shutil.rmtree(copy_labels_path_dst)
    if not os.path.exists(copy_labels_path_dst):
        os.makedirs(copy_labels_path_dst)

    np.random.seed(1010)
    indices = np.random.permutation(len(copy_images))
    src_files_samples = [copy_images[i] for i in indices[:number]]
    dst_files_samples = [os.path.join(copy_images_path_dst, os.path.split(file)[-1]) for file in src_files_samples]

    for src, dst in zip(src_files_samples, dst_files_samples):
        shutil.copyfile(src, dst)

    src_files_samples = [file_path.replace("/images", "/labels").replace(".jpg", ".json") for file_path in src_files_samples]
    dst_files_samples = [os.path.join(copy_labels_path_dst, os.path.split(file)[-1]) for file in src_files_samples]
    for src, dst in zip(src_files_samples, dst_files_samples):
        shutil.copyfile(src, dst)


copy_samples(train_scene_day, TRAIN_DAY_IMAGES_PATH, TRAIN_DAY_LABELS_PATH, Numbers_train)
copy_samples(train_scene_night, TRAIN_NIGHT_IMAGES_PATH, TRAIN_NIGHT_LABELS_PATH, Numbers_train)
copy_samples(val_scene_day, VAL_DAY_IMAGES_PATH, VAL_DAY_LABELS_PATH, Numbers_val)
copy_samples(val_scene_night, VAL_NIGHT_IMAGES_PATH, VAL_NIGHT_LABELS_PATH, Numbers_val)

print()