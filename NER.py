import tensorflow as tf
import numpy as np
from model import Model


class Config(object):
    # Holds the hyperparameters and data information.
    # The NRE_Model object are passed a Config() object at instantiation.
    n_relation = 53
    dropout = 0.5
    lr = 0.01
    embed_size = 50
    n_epochs = 50

class NRE_Model(Model):

    def __init__(self, config, pretrained_embeddings):
        # all kinds of embeddings with dict structure
        self.pretrained_embeddings = pretrained_embeddings
        self.config = config
        self.build()


