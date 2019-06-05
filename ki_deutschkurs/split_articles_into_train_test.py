#!/usr/bin/env python
# coding: utf-8

import csv
import collections
import numpy as np

from argparse import ArgumentParser
from sklearn.model_selection import train_test_split

""" split_articles_into_train_test.py:

processes the dataset and splits the dataset into a training- and testset
"""

SPLIT_TRAIN_TEST = .25
SPLIT_TRAIN_VAL = .2


def write_datasets(data, name, args):
    """ write a csv file in a normal and optinally in the fastText format """

    with open(name + ".csv", "w") as file_write:
        writer = csv.writer(file_write, delimiter=';', quotechar='\'', quoting=csv.QUOTE_MINIMAL)
        for row in data:
            writer.writerow(row)

    # optionally output files in the fastText format
    if args.fastText:
        with open("fastText_" + name + ".csv", "w") as file_write:
            writer = csv.writer(file_write, delimiter='\t', quotechar='\'', quoting=csv.QUOTE_MINIMAL)
            for row in data:
                label = row[0]
                label = "__label__" +  label
                writer.writerow([label, row[1]])


def read_dataset(name, cat_vs_rest=None):
    """ read csv_file """
    x = []
    y = []
    i = 0
    with open(name + ".csv", "r") as file_read:
        for line in file_read:
            i += 1
            xy = line.split(";", 2)
            if cat_vs_rest:
                label = xy[0]
                if label != cat_vs_rest:
                    xy[0] = "Andere"

            y += [xy[0]]
            x += [xy[1]]

    return x, y


if __name__ == "__main__":

    parser = ArgumentParser()
    parser.add_argument('-fastText', action='store_true')
    #parser.add_argument('-num_data',  metavar='num_data', const=-1,
    #                    type=int, help="Number of total datapoints (train, test and val)")
    args = parser.parse_args()

    labels = []
    texts = []

    # read full dataset file
    with open("articles.csv", "r") as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar='\'')
        for row in reader:
            labels.append(row[0])
            texts.append(row[1])

    n_subset = 1000
    n_data = len(labels)
    subset = np.random.choice(np.arange(n_data), n_subset, replace=False)

    print(subset)
    labels = [labels[i] for i in subset]
    texts = [texts[i] for i in subset]
    # split dataset in train/test
    trn_texts, tst_texts, trn_labels, tst_labels = train_test_split(texts, labels, test_size=SPLIT_TRAIN_TEST, random_state=42, stratify=labels)



    # split in train_val
    trn_texts, val_texts, trn_labels, val_labels = train_test_split(texts, labels, test_size=SPLIT_TRAIN_VAL,
                                                                    random_state=42, stratify=labels)
    # write train and test datasets
    train = []
    val = []
    test = []
    
    for i in range(len(trn_labels)):
        train.append([trn_labels[i], trn_texts[i]])

    for i in range(len(val_labels)):
        val.append([val_labels[i], val_texts[i]])

    for i in range(len(tst_labels)):
        test.append([tst_labels[i], tst_texts[i]])

    write_datasets(train, "train", args)
    write_datasets(val, "val", args)
    write_datasets(test, "test", args)


