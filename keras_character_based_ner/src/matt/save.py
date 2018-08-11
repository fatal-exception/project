from keras_character_based_ner.src.model import CharacterBasedLSTMModel


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


