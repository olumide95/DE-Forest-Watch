import os
import random
import shutil
import tempfile


def move_subset(src, size=200):
    with tempfile.TemporaryDirectory() as tmp:
        files = os.listdir(src)
        subset = []

        while size:
            choice = random.choice(files)
            subset.append(files.pop(files.index(choice)))
            size -= 1

        for i in subset:
            fsrc = os.path.join(src, i)
            dest = os.path.join(tmp, i)
            shutil.copy(fsrc, dest)

        shutil.rmtree(src)
        os.makedirs(src)
        for i in os.listdir(tmp):
            fsrc = os.path.join(tmp, i)
            fdest = os.path.join(src, i)
            shutil.copy(fsrc, fdest)


if __name__ == "__main__":
    move_subset("/home/abraham/ForestWatch/DE-Forest-Watch/ml/data/svm/deforest")
    move_subset("/home/abraham/ForestWatch/DE-Forest-Watch/ml/data/svm/forest")

