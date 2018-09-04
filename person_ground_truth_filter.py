import os
from glob import glob

ROOT_PATH = os.path.split(os.getcwd())[0]
mAP_PATH = os.path.join(ROOT_PATH, 'mAP_person')
GROUND_TRUTH_PATH = os.path.join(mAP_PATH, 'ground-truth')
files = glob(GROUND_TRUTH_PATH + '/*.txt')

for file in files:
    with open(file) as f:
        lines = f.readlines()
        save_lines = []
        for line in lines:
            obj = line.split()[0]
            if obj == 'person':
                save_lines.append(line)
    with open(file, 'w') as f:
        f.writelines(save_lines)

