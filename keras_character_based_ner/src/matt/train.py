from keras_character_based_ner.src.config import Config
from keras_character_based_ner.src.dataset import CharBasedNERDataset
from keras_character_based_ner.src.model import CharacterBasedLSTMModel
from keras_character_based_ner.src.matt.model_integration import get_x_y as matt_get_x_y


def toy_dataset_fit():
    config = Config()

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
    dataset = ToyCharBasedNERDataset()
    model = CharacterBasedLSTMModel(config, dataset)

    model.fit()
    model.evaluate()
    print(model.predict_str('My name is Margaret Thatcher, and I greatly enjoy shopping at Tesco when I am in Birmingham!'))
    model.save("keras_character_based_ner/src/toy_dataset.keras")


def mini_dataset_fit():
    config = Config()

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
    model = CharacterBasedLSTMModel(config, dataset)

    model.fit()
    model.evaluate()
    print(model.predict_str('My name is Margaret Thatcher, and I greatly enjoy shopping at Tesco when I am in Birmingham!'))
    model.save("keras_character_based_ner/src/mini_dataset.keras")
