from keras_character_based_ner.src.model import CharacterBasedLSTMModel
from keras_character_based_ner.src.dataset import CharBasedNERDataset
from keras_character_based_ner.src.matt.file_management import unpickle_large_file
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
        :param x_test: x of the test dataset
        :param y_test: y of the test dataset
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

    def predict_long_str(self, s: str):
        """
        Override CharacterBasedLSTMModel's own predict_str. This is because
        we want to be able to predict strings that are longer than config.sentence_max_length.
        Other than setting the 2nd argument of str_to_x to 'sys.maxsize', the rest is unchanged
        from the original predict_str function.
        :param s:
        :return:
        """
        x = self.dataset.str_to_x(s, len(s))
        predicted_classes = self.predict_x(x)
        chars = self.dataset.x_to_str(x)[0]
        labels = self.dataset.y_to_labels(predicted_classes)[0]

        return list(zip(chars, labels))


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


class AlphabetPreloadedCharBasedNERDataset(CharBasedNERDataset):
    """
    A version of CharBasedNERDataset where we don't need to create an alphabet dynamically
    by unioning together a set of texts. This means a. it's quicker to load the whole model
    and b. we can run the model independently of having the texts to hand.
    """
    def __init__(self):
        print("Using pickled alphabet for dataset")
        self.alphabet = unpickle_large_file("keras_character_based_ner/src/alphabet.p")
        self.labels = self.BASE_LABELS + self.get_labels()
        self.num_labels = len(self.labels)
        self.num_to_label = {}
        self.label_to_num = {}
        self.init_mappings()
