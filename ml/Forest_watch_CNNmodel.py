import os

from keras.applications import DenseNet201 as DenseNet
from keras.applications.densenet import preprocess_input
from keras.models import load_model
from keras.preprocessing.image import ImageDataGenerator

DATA_PATH = "da"
TRAIN_DATA_PATH = os.path.join(DATA_PATH, "train")
VALIDATION_DATA_PATH = os.path.join(DATA_PATH, "eval")
TEST_DATA_PATH = os.path.join(DATA_PATH, "test")

MODEL_PATH = os.path.join(DATA_PATH, "model2.h5")

model = DenseNet(include_top=True, weights=None, classes=3)
image_generator = ImageDataGenerator(preprocessing_function=preprocess_input)

model.compile(
        optimizer="adam",
        loss="categorical_crossentropy",
        metrics=["accuracy", "categorical_accuracy"],
    )
model.fit_generator(image_generator.flow_from_directory(TRAIN_DATA_PATH, target_size=(224, 224)),
        steps_per_epoch=2,
        epochs=5,
        validation_data=image_generator.flow_from_directory(
            VALIDATION_DATA_PATH, target_size=(224, 224)
        ),
        validation_steps=1,
    )

model.save(MODEL_PATH)