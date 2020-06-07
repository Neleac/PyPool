import csv
import os
import random

data_dir = "/home/wangc21/datasets/pool/images"


train_rows = []
test_rows = []

for _, dirs, _ in os.walk(data_dir):
    for folder in dirs:

        label = int(folder.split("_")[0])

        '''
        if label == 0:
            # cue ball
            label = 0
        elif label == 8:
            # eight ball
            label = 1
        elif label < 8:
            # solids
            label = 3
        else:
            # stripes
            label = 4
        '''

        for _, _, files in os.walk(os.path.join(data_dir, folder)):
            for img in files:

                path = "%s/%s" % (folder, img)

                # train-test-split, 80% train, 20% test
                if random.random() < 0.8:
                    train_rows.append([path, label])
                else:
                    test_rows.append([path, label])


with open(os.path.join(data_dir, "train_labels.csv"), mode = "w") as train_labels:
    csv_writer = csv.writer(train_labels, delimiter = ",")
    csv_writer.writerows(train_rows) 

with open(os.path.join(data_dir, "test_labels.csv"), mode = "w") as test_labels:
    csv_writer = csv.writer(test_labels, delimiter = ",")
    csv_writer.writerows(test_rows)
