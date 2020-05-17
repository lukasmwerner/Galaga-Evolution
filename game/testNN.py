import numpy as np
import NeuralNet as nn
inputs = [0,0,0,1]
outputs = [0,0,0]
ins = np.asarray(inputs, dtype=np.float32)
outs = np.asarray(outputs, dtype=np.float32)
brain = nn.Brain(ins, outs)
print(brain.predict(0,0,0))