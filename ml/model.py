# -*- coding: utf-8 -*-
import os

import numpy as np
import skimage.io as io
from sklearn.externals import joblib
from sklearn.model_selection import StratifiedKFold, cross_val_score
import sklearn.svm as svm
from skimage.transform import resize
from sklearn.preprocessing import scale
from sklearn.utils import Bunch


DATASET = None

IMAGE_DATA_DIR = os.path.join(os.path.dirname(__file__), "data", "svm")
MODEL_FILE = os.path.join(os.path.dirname(__file__), "svm.pkl")


def load_data(directory, target_size=(200, 200), ext="jpg"):
    labels = [i for i in os.listdir(directory) if not i.startswith(".")]
    labels, indices = np.unique(sorted(labels), return_inverse=True)
    index_map = {k: v for k, v in zip(labels, indices)}

    data, targets = [], []
    for label in labels:
        label_path = os.path.join(directory, label)
        images = [i for i in os.listdir(label_path) if i.lower().endswith(ext.lower())]

        for filename in images:
            filename = os.path.join(label_path, filename)

            image = resize(io.imread(filename), target_size)

            data.append(image)
            targets.append(index_map[label])

    data = np.stack(data)

    targets = np.array(targets)
    target_names = np.array(labels)

    return Bunch(data=data, target=targets, target_names=target_names)


def load_X_y():
    global DATASET
    if not DATASET:
        DATASET = load_data(IMAGE_DATA_DIR)
    X, y = DATASET.data.reshape(len(DATASET.data), -1), DATASET.target
    return X, y


def load_sample_image(filepath, target_size=(200, 200)):
    """
    Load a single image as a sample for passing to the `predict` method of a model.
    """
    image = resize(io.imread(filepath), target_size)

    # the model expects a sample of images, convert the single image to a
    # sample of length 1
    sample = np.expand_dims(image, axis=0)
    sample = sample.reshape(len(sample), -1)

    return sample


def create_model():
    try:
        return joblib.load(MODEL_FILE)
    except:
        pass

    X, y = load_X_y()
    estimator = svm.SVC(kernel="linear")
    cv = StratifiedKFold(n_splits=3)
    scores = cross_val_score(estimator, X, y, cv=cv, n_jobs=-1)

    print("Accuracy: {:0.4f} (+/- {:0.4f})".format(scores.mean(), scores.std() * 2))

    estimator.fit(X, y)

    joblib.dump(estimator, MODEL_FILE)

    return estimator


def predict(image_path):
    estimator = create_model()
    sample = load_sample_image(image_path)

    prediction = estimator.predict(sample)[0]

    return "Forest" if prediction == 1 else "Not Forest"


if __name__ == "__main__":
    forest = "/home/abraham/ForestWatch/DE-Forest-Watch/ml/data/test/MatureForest/vegetation1707.jpg"
    print(predict(forest))

    deforest = "/home/abraham/ForestWatch/DE-Forest-Watch/ml/data/test/Deforested/dirt1_13-3-164.jpg"
    print(predict(deforest))

