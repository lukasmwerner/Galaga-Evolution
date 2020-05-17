import numpy as np
import random

def activation(item):
    for x in item:
        if x > 0:
            x = 1
        else:
            x = 0
    return item

class Brain(object):
    def __init__(self, inputs, outputs):
        if type(inputs) == list:
            inputs = np.asarray(inputs, dtype=np.float32)
        if type(outputs) == list:
            outputs = np.asarray(outputs, dtype=np.float32)

        self.inputs = inputs
        self.weights1 = np.random.rand(self.inputs.shape[0], 4)
        self.weights2 = np.random.rand(4,outputs.shape[0])
        self.y = outputs
        self.output = np.zeros(outputs.shape)

    def predict(self, nearestEnemyX, nearestEnemyY, currentX):
        self.inputs = np.asarray([nearestEnemyX, nearestEnemyY, currentX])
        self.layer1 = activation(np.dot(self.inputs, self.weights1))
        self.output = activation(np.dot(self.layer1, self.weights2))
        return self.output

    def mutate(self, amt):
        for i in range(0, amt):
            self.weights1[random.choice(range(0, 3))] += random.randrange(-10, 10) / 10
            self.weights2[random.choice(range(0, 4))] += random.randrange(-10, 10) / 10