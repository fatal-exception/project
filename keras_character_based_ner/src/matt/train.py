from keras_character_based_ner.src.config import Config
from keras_character_based_ner.src.dataset import CharBasedNERDataset
from keras_character_based_ner.src.matt.model_integration import get_x_y as matt_get_x_y
from keras_character_based_ner.src.matt.file_management import pickle_large_file
from keras_character_based_ner.src.matt.persist import LoadedToyModel, SavedCharacterBasedLSTMModel


class ToyConfig(Config):
    """
    Override Config with something suitable for toy testing - i.e. only a few epochs
    """
    max_epochs = 8


class ToyCharBasedNERDataset(CharBasedNERDataset):
    def get_x_y(self, sentence_maxlen, dataset_name='all'):
        """
        Override super-class definition in CharBasedNERDataset so we use toy data, not mini data
        :param self:
        :param sentence_maxlen:
        :param dataset_name:
        :return:
        """
        return matt_get_x_y(dataset_name, "toy")


def toy_dataset_fit():
    print("Fitting toy dataset")
    config = ToyConfig()
    dataset = ToyCharBasedNERDataset()
    model = SavedCharacterBasedLSTMModel(config, dataset)

    history = model.fit()
    history_dict = history.history
    model.evaluate()
    print(model.predict_str('My name is Margaret Thatcher, and I greatly enjoy shopping at Tesco when I am in Birmingham!'))
    model.save("keras_character_based_ner/src/toy_dataset.keras.h5")
    pickle_large_file(history_dict, "keras_character_based_ner/src/toy_dataset.history.p")


def toy_dataset_refit():
    """
    Continue training on toy dataset after loading in from disk
    :return:
    """
    config = ToyConfig()
    dataset = ToyCharBasedNERDataset()
    model = LoadedToyModel(config, dataset)

    history = model.fit()
    history_dict = history.history
    model.evaluate()
    print(model.predict_str('My name is Margaret Thatcher, and I greatly enjoy shopping at Tesco when I am in Birmingham!'))
    model.save("keras_character_based_ner/src/toy_dataset.keras.h5")
    pickle_large_file(history_dict, "keras_character_based_ner/src/toy_dataset.history.p")


def mini_dataset_fit():
    class MiniConfig(Config):
        """
        Override Config with something suitable for quick testing - i.e. only a few epochs
        """
        max_epochs = 2

    config = MiniConfig()

    class MiniCharBasedNERDataset(CharBasedNERDataset):
        def get_x_y(self, sentence_maxlen, dataset_name='all'):
            """
            Override super-class definition in CharBasedNERDataset so we use mini data, not toy data.
            :param self:
            :param sentence_maxlen:
            :param dataset_name:
            :return:
            """
            return matt_get_x_y(dataset_name, "mini")

    dataset = MiniCharBasedNERDataset()
    model = SavedCharacterBasedLSTMModel(config, dataset)

    history = model.fit()
    history_dict = history.history
    model.evaluate()
    print(model.predict_str('My name is Margaret Thatcher, and I greatly enjoy shopping at Tesco when I am in Birmingham!'))
    model.save("keras_character_based_ner/src/mini_dataset.keras.h5")
    pickle_large_file(history_dict, "keras_character_based_ner/src/mini_dataset.history.p")


def full_dataset_fit_generator():
    print("Fitting full dataset using generator")
    config = Config()
    dataset = CharBasedNERDataset()
    model = SavedCharacterBasedLSTMModel(config, dataset)

    history = model.fit_generator()
    history_dict = history.history
    model.evaluate_generator()
    print(model.predict_str('My name is Margaret Thatcher, and I greatly enjoy shopping at Tesco when I am in Birmingham!'))
    model.save("keras_character_based_ner/src/full_dataset.keras.h5")
    pickle_large_file(history_dict, "keras_character_based_ner/src/full_dataset.history.p")
