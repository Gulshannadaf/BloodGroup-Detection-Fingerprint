import os
#import random

import cv2
import numpy as np
from PIL import Image

#import pandas as pd
#import seaborn as sns
#import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

from tensorflow import keras
from keras import layers, models
#from keras.preprocessing.image import img_to_array, load_img
from tensorflow.keras.utils import img_to_array, load_img
from keras.utils import to_categorical

# from tensorflow import keras
# from tensorflow.keras import layers 
# from tensorflow.keras import layers, models
# from tensorflow.keras.utils import to_categorical

img = cv2.imread("Data\A-\cluster_1_0 - Copy.BMP")
cv2.imshow("Image",img)
cv2.waitKey(0)
print(img.shape)
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imshow("Image",img)
cv2.waitKey(0)
print(img.shape)
img = np.expand_dims(img, axis=-1)
img = cv2.equalizeHist(img)
cv2.imshow("Image",img)
cv2.waitKey(0)
print(img.shape)

clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(4, 4))
img = clahe.apply(img)
cv2.imshow("Image",img)
cv2.waitKey(0)

alpha = 2.5  # Increase the contrast (1.0 - 3.0)
beta = 0     # Brightness control (0-100)
img = cv2.convertScaleAbs(img, alpha=alpha, beta=beta)
cv2.imshow("Image",img)
cv2.waitKey(0)


