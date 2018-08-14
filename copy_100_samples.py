import os
import shutil
import numpy as np
from shutil import copyfile


DATASET_PATH = os.path.split(os.getcwd())[0]


def copy_samples(copy_path_src, copy_path_dst):
    if os.path.exists(copy_path_dst):   # if it exist already
      shutil.rmtree(copy_path_dst)

    if not os.path.exists(copy_path_dst):
        os.makedirs(copy_path_dst)

    src_files = os.listdir(copy_path_src)
    indices = np.random.permutation(len(src_files))
    src_files_samples = [src_files[i] for i in indices[:100]]

    dst_files_samples = [os.path.join(copy_path_dst, file) for file in src_files_samples]
    src_files_samples = [os.path.join(copy_path_src, file) for file in src_files_samples]

    for src, dst in zip(src_files_samples, dst_files_samples):
        copyfile(src, dst)
    return src_files_samples, dst_files_samples


if __name__ == '__main__':
    # copy night
    copy_path_src = os.path.join(DATASET_PATH, "BDD/day_night_separate/images/val/night")
    copy_path_dst = copy_path_src + '_100'
    src_files_samples, dst_files_samples = copy_samples(copy_path_src, copy_path_dst)

    # copy SID_Sony
    copy_path_dst = os.path.join(DATASET_PATH, "BDD/day_night_separate/images/val/SID_Sony_100")
    if os.path.exists(copy_path_dst):   # if it exist already
      shutil.rmtree(copy_path_dst)
    if not os.path.exists(copy_path_dst):
        os.makedirs(copy_path_dst)
    sid_src = [file_path.replace("/night", "/SID_Sony") for file_path in src_files_samples]
    sid_dst = [file_path.replace("/night", "/SID_Sony") for file_path in dst_files_samples]
    for src, dst in zip(sid_src, sid_dst):
        copyfile(src, dst)

    # copy DPED
    copy_path_dst = os.path.join(DATASET_PATH, "BDD/day_night_separate/images/val/DPED_100")
    if os.path.exists(copy_path_dst):   # if it exist already
      shutil.rmtree(copy_path_dst)
    if not os.path.exists(copy_path_dst):
        os.makedirs(copy_path_dst)
    dped_src = [file_path.replace("/night", "/DPED").replace('.jpg', '.png') for file_path in src_files_samples]
    dped_dst = [file_path.replace("/night", "/DPED").replace('.jpg', '.png') for file_path in dst_files_samples]
    for src, dst in zip(dped_src, dped_dst):
        copyfile(src, dst)

    # copy labels
    copy_path_dst = os.path.join(DATASET_PATH, "BDD/day_night_separate/labels/val/night_bdd2mAP_100")
    if os.path.exists(copy_path_dst):   # if it exist already
      shutil.rmtree(copy_path_dst)
    if not os.path.exists(copy_path_dst):
        os.makedirs(copy_path_dst)
    labels_src = [file_path.replace("/images", "/labels").replace("/night", "/night_bdd2mAP").replace('.jpg', ".txt") for file_path in src_files_samples]
    labels_dst = [file_path.replace("/images", "/labels").replace("/night", "/night_bdd2mAP").replace('.jpg', ".txt") for file_path in dst_files_samples]
    for src, dst in zip(labels_src, labels_dst):
        copyfile(src, dst)
