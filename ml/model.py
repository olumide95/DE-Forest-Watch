import pathlib

from keras.applications import DenseNet201 as DenseNet
from keras.applications.densenet import preprocess_input
from keras.models import load_model
from keras.preprocessing.image import ImageDataGenerator

TRAIN_DATA_PATH = "Kaggle_Dataset/Data/Train"
VALIDATION_DATA_PATH = "Kaggle_Dataset/Data/Eval"
TEST_DATA_PATH = "Kaggle_Dataset/Data/Test"
MODEL_PATH = "model.h5"


def initialize_model(reinitialize=False):
    """Initialize a machine learning model for image classification.
    
    Args:
        reinitialize (boolean): Indicates if the model should be loaded
            from a saved model file or retrained from scratch. If there
            is not presaved model a new model is trained.
    
    Returns:
        keras.Model: a prefitted model instance.
    """
    if not reinitialize:
        model_file = pathlib.Path(MODEL_PATH)
        model_exists = model_file.exists() and model_file.is_file()
        if model_exists:
            return load_model(MODEL_PATH)

    model = DenseNet(include_top=True, weights=None, classes=3)
    image_generator = ImageDataGenerator(preprocessing_function=preprocess_input)

    model.compile(
        optimizer="adam",
        loss="categorical_crossentropy",
        metrics=["accuracy", "categorical_accuracy"],
    )
    model.fit_generator(
        image_generator.flow_from_directory(TRAIN_DATA_PATH, target_size=(224, 224)),
        steps_per_epoch=1,
        epochs=5,
        validation_data=image_generator.flow_from_directory(
            VALIDATION_DATA_PATH, target_size=(224, 224)
        ),
        validation_steps=1,
    )

    model.save(MODEL_PATH)

    return model


def predict(sample):
    """Predict the class of all images in the sample.
    
    Args:
        sample (numpy.array): A numpy array of images to be predicted.
    
    Returns:
        list
    """
    model = initialize_model()
    sample = preprocess_input(sample)

    return model.predict(sample)
