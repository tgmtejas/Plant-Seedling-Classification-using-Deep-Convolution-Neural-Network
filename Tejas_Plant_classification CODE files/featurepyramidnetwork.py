# -*- coding: utf-8 -*-
"""FeaturePyramidNetwork.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1O7NoSuoIr49vujeHEDsxMd7fD7LYU6mV
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# %matplotlib inline

from sklearn.model_selection import train_test_split
import itertools
from keras.layers.core import Lambda
from keras.preprocessing import image
from keras.layers.core import Dropout, Lambda
from keras.preprocessing.image import ImageDataGenerator
from keras.callbacks import ReduceLROnPlateau
from keras.models import Sequential, Model
from keras.layers import Dense, Activation, Flatten, Dropout, concatenate, Input, Conv2D, MaxPooling2D, Conv2DTranspose
from keras.optimizers import Adam, Adadelta
from keras.callbacks import EarlyStopping, ModelCheckpoint
from keras.layers.advanced_activations import LeakyReLU

import scipy.io as sio
My_data = sio.loadmat('drive/Plant Classification Using C-CNN/train/Image_Processed_1data.mat')
x_train = My_data['train']
labels = My_data["train_labels"]

x_train, x_val, y_train, y_val = train_test_split(x_train, labels, test_size = 0.1, random_state=10, stratify=labels)
x_train, x_test, y_train, y_test = train_test_split(x_train, y_train, test_size = 0.1, random_state=10, stratify =y_train)

print('Train data:', len(x_train), ', Test data:', len(x_test), ', Train labels:', len(y_train), ', Test labels:', len(y_test))

input_shape = x_train[1].shape
print('Input Shape is :', input_shape)

#Model

def Conv_layer(filter_size, inp):
  cv1 = Conv2D(filter_size, (3,3), padding='same')(inp)
  cv1 = LeakyReLU(alpha=0.15)(cv1)
  cv1 = Dropout(0.1)(cv1)
  cv1 = Conv2D(filter_size, (3,3), padding='same')(cv1)
  out = LeakyReLU(alpha=0.15)(cv1)
  return out
  
def Pooling(inp):
  mp1 = MaxPooling2D((2, 2))(inp)
  return mp1


#cv2 = Conv2D(16, (3,3), padding='same')(mp1)
#cv2 = LeakyReLU(alpha=0.15)(cv2)
#cv2 = Dropout(0.1)(cv2)
#cv2 = Conv2D(16, (3,3), padding='same')(cv2)
#cv2 = LeakyReLU(alpha=0.15)(cv2)
#mp2 = MaxPooling2D((2, 2))(cv2)

def Upsampling(filter_size, inp, feedforward):
  up1 = Conv2DTranspose(filter_size, (2, 2), strides=(2, 2), padding='same') (inp)
  up1 = concatenate([up1, feedforward])
  up1 = Conv2D(filter_size, (3,3), padding='same')(up1)
  up1 = LeakyReLU(alpha=0.15)(up1)
  up1 = Dropout(0.1)(up1)
  up1 = Conv2D(filter_size, (3,3), padding='same')(up1)
  out = LeakyReLU(alpha=0.15)(up1)
  return out

image_input=Input(shape=input_shape)
ip = Lambda(lambda x: x / 255) (image_input)

l1 = Conv_layer(8, ip)
p1 = Pooling(l1)

l2 = Conv_layer(16, p1)
p2 = Pooling(l2)

l3 = Conv_layer(32, p2)
p3 = Pooling(l3)

l4 = Conv_layer(64, p3)

u1 = Upsampling(32, l4, l3)
u2 = Upsampling(16, u1, l2)
u3 = Upsampling(8, u2, l1)

d1 = Flatten()(u3)
d1 = Dense(512)(d1)
d1 = Dropout(0.5)(d1)
d1 = LeakyReLU(alpha=0.1)(d1)

d2 = Dense(256)(d1)
d2 = Dropout(0.2)(d2)
d2 = LeakyReLU(alpha=0.1)(d2)

out = Dense(12, activation='softmax')(d2)

model_new = Model(image_input, out)
model_new.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
model_new.summary()

#earlystopper = EarlyStopping(monitor='val_loss', patience=15, verbose=1)
#checkpointer = ModelCheckpoint('drive/Plant Classification Using C-CNN/Models/FPN/FPN1.h5.h5', monitor='val_acc', verbose=1, save_best_only=True)
history = model_new.fit(x_train, y_train,validation_split=0.1, epochs=7, batch_size=50)

y_val_pred = model_new.evaluate(x_val, y_val, batch_size=32, verbose=1, sample_weight=None)

print()
print ("Validation Loss = " + str(y_val_pred[0]))
print ("Validation Accuracy = " + str(y_val_pred[1]))

y_test_pred = model_new.evaluate(x_test, y_test, batch_size=32, verbose=1, sample_weight=None)

print()
print ("Test Loss = " + str(y_test_pred[0]))
print ("Test Accuracy = " + str(y_test_pred[1]))

y_train_pred = model_new.evaluate(x_train, y_train, batch_size=32, verbose=1, sample_weight=None)

print()

print ("Train Loss = " + str(y_train_pred[0]))
print ("Train Accuracy = " + str(y_train_pred[1]))

y_train_pred =model_new.predict(x_train, batch_size=64, verbose=1, steps=None)
y_test_pred =model_new.predict(x_test, batch_size=64, verbose=1, steps=None)
y_val_pred =model_new.predict(x_val, batch_size=64, verbose=1, steps=None)

y_train_pred = np.argmax(y_train_pred, axis=1)
y_test_pred = np.argmax(y_test_pred, axis=1)
y_val_pred = np.argmax(y_val_pred, axis=1)

y_train_x = np.argmax(y_train, axis=1)
y_test_x = np.argmax(y_test, axis=1)
y_val_x = np.argmax(y_val, axis=1)

from sklearn.metrics import confusion_matrix
SPECIES = ['Black-grass', 'Charlock', 'Cleavers', 'Common Chickweed', 'Common wheat', 'Fat Hen',
              'Loose Silky-bent', 'Maize', 'Scentless Mayweed', 'Shepherds Purse',
              'Small-flowered Cranesbill', 'Sugar beet']

def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Confusion matrix")
    else:
        print('Classification Matrix')

    print(cm)

    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')

# Compute confusion matrix for Train
cnf_matrix = confusion_matrix(y_train_x, y_train_pred)
np.set_printoptions(precision=2)

# Plot non-normalized confusion matrix
plt.figure()
plot_confusion_matrix(cnf_matrix, classes=SPECIES,
                      title='Classification matrix')

# Plot normalized confusion matrix
plt.figure()
plot_confusion_matrix(cnf_matrix, classes=SPECIES, normalize=True,
                      title='Confusion matrix')



plt.show()

# Compute confusion matrix
cnf_matrix = confusion_matrix(y_test_x, y_test_pred)
np.set_printoptions(precision=2)

# Plot non-normalized confusion matrix
plt.figure()
plot_confusion_matrix(cnf_matrix, classes=SPECIES,
                      title='Confusion matrix')

# Plot normalized confusion matrix
plt.figure()
plot_confusion_matrix(cnf_matrix, classes=SPECIES, normalize=True,
                      title='Normalized confusion matrix')

plt.show()

# Compute confusion matrix
cnf_matrix = confusion_matrix(y_val_x, y_val_pred)
np.set_printoptions(precision=2)

# Plot non-normalized confusion matrix
plt.figure()
plot_confusion_matrix(cnf_matrix, classes=SPECIES,
                      title='Confusion matrix')

# Plot normalized confusion matrix
plt.figure()
plot_confusion_matrix(cnf_matrix, classes=SPECIES, normalize=True,
                      title='Normalized confusion matrix')

plt.show()

from matplotlib import axes as plt2
from matplotlib import pyplot as plt
# summarize history for accuracy
plt.plot(history.history['acc'])
plt.plot(history.history['val_acc'])
#plt.plot(history.history['loss'])
plt.title('Model accuracy graph')
plt.ylabel('Accuracy')

plt.xlabel('Epoch')
plt.legend(['Accuracy'], loc='upper centre')
plt.show()
# summarize history for loss
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('Model loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(['train', 'test'], loc='upper left')

plt.show()