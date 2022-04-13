import numpy as np
import pandas as pd
import os
import cv2
import matplotlib.pyplot as plt
import os
from PIL import Image
from keras.preprocessing.image import img_to_array
from keras.preprocessing.image import load_img
from keras.utils import np_utils
from tensorflow.python.keras.layers import Dense,Conv2D,Flatten,MaxPooling2D,GlobalAveragePooling2D,Activation,BatchNormalization,Dropout
from tensorflow.python.keras import Sequential,backend,optimizers

uninfected_data = os.listdir('D:\\backups\\ManiyoorMaleria\\maniyoormalaria\\maniyoormalaria\\cell_images\\cell_images\\Uninfected\\')
parasitized_data = os.listdir('D:\\backups\\ManiyoorMaleria\\maniyoormalaria\\maniyoormalaria\\cell_images\\cell_images\\Parasitized\\')
data = []
labels = []

for img in parasitized_data:
    try:
        img_read = plt.imread('D:\\backups\\ManiyoorMaleria\\maniyoormalaria\\maniyoormalaria\\cell_images\\cell_images\\' + img)
        img_resize = cv2.resize(img_read, (50, 50))
        img_array = img_to_array(img_resize)
        data.append(img_array)
        labels.append(1)
    except:

        None

for img in uninfected_data:
    print(img)
    try:
        img_read = plt.imread('D:\\backups\\ManiyoorMaleria\\maniyoormalaria\\maniyoormalaria\\cell_images\\cell_images\\' + img)
        img_resize = cv2.resize(img_read, (50, 50))
        img_array = img_to_array(img_resize)
        data.append(img_array)
        labels.append(0)
    except:
        None

image_data = np.array(data)
labels = np.array(labels)


print(image_data,labels)




print("image_data:", len(image_data))
print("labels:", len(labels))