from keras_character_based_ner.src.model import CharacterBasedLSTMModel
from typing import Callable, Dict
from keras.models import load_model, Sequential  # type: ignore


class SavedCharacterBasedLSTMModel(CharacterBasedLSTMModel):
    def __init__(self, config, dataset):
        super().__init__(config, dataset)

    def save(self, filepath):
        """
        MIR Added method to save model to disk
        :param filepath: file path under which to save
        :return:
        """
        return self.model.save(filepath)

    def manual_evaluate(self, x_test, y_test, batch_size):
        """
        Provide a hook to manually run model.evaluate() without needing to create
        a new Dataset object each time. Useful for cross-fold evaluation.
        :param x: x of the test dataset
        :param y: y of the test dataset
        :param batch_size:
        :return:
        """
        return self.model.evaluate(x=x_test, y=y_test, batch_size=batch_size)

    def manual_fit(self, x_train, y_train, batch_size, epochs):
        """
        Provide a hook to manually run model.fit() without needing
        to create a new Dataset object each time. Useful for cross-fold evaluation.
        :param x_train:
        :param y_train:
        :param batch_size:
        :param epochs:
        :return:
        """
        return self.model.fit(x=x_train,
                              y=y_train,
                              batch_size=batch_size,
                              epochs=epochs,
                              verbose=1
                              )


class LoadedToyModel(SavedCharacterBasedLSTMModel):
    """
    A loaded model with all the functionality of a CharacterBasedLSTMModel
    """
    def get_model(self):
        print("Loading in model from previous training of Toy dataset")
        model_path = "keras_character_based_ner/src/toy_dataset.keras.h5"
        custom_objects: Dict[str, Callable] = {
            'non_null_label_accuracy': SavedCharacterBasedLSTMModel.non_null_label_accuracy
        }
        model: Sequential = load_model(model_path, custom_objects=custom_objects)
        print("Completed loading in model from previous training of Toy dataset")
        return model


class LoadedMiniModel(SavedCharacterBasedLSTMModel):
    """
    A loaded model with all the functionality of a CharacterBasedLSTMModel
    """
    def get_model(self):
        print("Loading in model from previous training of Mini dataset")
        model_path = "keras_character_based_ner/src/mini_dataset.keras.h5"
        custom_objects: Dict[str, Callable] = {
            'non_null_label_accuracy': SavedCharacterBasedLSTMModel.non_null_label_accuracy
        }
        self.model: Sequential = load_model(model_path, custom_objects=custom_objects)
