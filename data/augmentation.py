import cv2
import os
import random

data_dir = "/home/wangc21/datasets/pool/images"

for _, dirs, _ in os.walk(data_dir):
    for folder in dirs:
        print(folder)
        for _, _, files in os.walk(os.path.join(data_dir, folder)):
            imgs = files

        n_samples = 1000 - len(imgs)

        for i in range(n_samples):
            sample = random.choice(imgs)
            idx = sample.split(".")[0]

            image = cv2.imread(os.path.join(data_dir, folder, sample))
            image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
            cv2.imwrite(os.path.join(data_dir, folder, "%s_%d.png" % (idx, i)), image)
