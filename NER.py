import tensorflow as tf
import numpy as np
from model import Model
import os


class Config(object):
    # Holds the hyperparameters and data information.
    # The NRE_Model object are passed a Config() object at instantiation.
    n_relation = 53
    dropout = 0.5
    lr = 0.01
    w_embed_size = 50
    p_embed_size = 10
    n_epochs = 50
    n_features = w_embed_size + 2 * p_embed_size


class NRE_Model(Model):

    def __init__(self, config, pretrained_embeddings):
        # all kinds of embeddings with dict structure
        self.pretrained_embeddings = pretrained_embeddings
        self.config = config
        self.build()

    def add_placeholders(self):
        n_features = self.config.n_features
        # self.input_placeholder = tf.placeholder()


def main():
    # read in data
    path = "./data/"
    word_embedding = np.load(path+ "vec.npy")
    train_sen = np.load(path + "train_sen")
    train_ans = np.load(path + "train_ans")
    test_sen = np.load(path + "test_sen")
    test_ans = np.load(path + "test_ans")
    train_target = np.load(path+"train_target")
    test_target = np.load(path + "test_target")


if __name__ == "__main__":
    main()

