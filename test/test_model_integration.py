from keras_character_based_ner.src.matt.model_integration import onehot


def test_onehot():
    result = onehot(4, 7)
    expected = [0, 0, 0, 0, 1, 0, 0]
    assert result == expected

