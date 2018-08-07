from keras_character_based_ner.src.matt.file_management import unpickle_large_file
from typing import Dict

# Examples in this file taken from
# Deep Learning with Python
# by François Chollet
# Published by Manning Publications, 2017
# Chapter 6 'Deep learning for text and sequences'


def graph_model_history(filepath, dest_file_name):
    import matplotlib
    matplotlib.use('TkAgg')
    import matplotlib.pyplot as plt
    history_dict = unpickle_large_file(filepath)

    cat_acc = history_dict['categorical_accuracy']
    non_null_label_acc = history_dict['non_null_label_accuracy']
    loss = history_dict['loss']
    val_loss = history_dict['val_loss']
    val_cat_acc = history_dict['val_categorical_accuracy']
    val_non_null_label_acc = history_dict['val_non_null_label_accuracy']

    epochs = range(1, len(cat_acc) + 1)

    plt.plot(epochs, cat_acc, 'bo', label='Training acc')
    plt.plot(epochs, val_cat_acc, 'b', label='Validation acc')
    plt.title('Training and validation accuracy')
    plt.legend()

    plt.figure()

    plt.plot(epochs, loss, 'bo', label='Training loss')
    plt.plot(epochs, val_loss, 'b', label='Validation loss')
    plt.title('Training and validation loss')
    plt.legend()

    plt.savefig('keras_character_based_ner/src/{}'.format(dest_file_name))
