import numpy as np
class activation_function():
    def __init__(self, x_func, y_func):
        self.x = x_func
        self.y = y_func

    @staticmethod
    def sigmoid():
        return activation_function(
            lambda x, i, j: 1 / (1 + np.exp(-x)),
            lambda y, i, j: y * (1-y)
        )

    @staticmethod
    def tanh():
        return activation_function(
            lambda x, i, j: np.tanh(x),
            lambda y, i, j: 1-(y*y)
        )
