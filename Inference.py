import os
from RunPridiction import makePrediction
import numpy as np
from keras.models import load_model

model = load_model("test1.h5")


prediction = np.array(makePrediction(model,'Data\A-\cluster_1_67.BMP'))
np.set_printoptions(suppress=True,linewidth=10)
print (prediction)