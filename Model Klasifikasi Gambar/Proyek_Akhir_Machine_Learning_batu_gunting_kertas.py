# -*- coding: utf-8 -*-
"""Copy of Proyek Akhir Machine Learning.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1bAR6YrKKGaoPs0s5kMhIsaDscl6qefFq

Import tensorflow
"""

import tensorflow as tf
print(tf.__version__)

"""Download dataset dari DICODING Academy"""

!wget --no-check-certificate \
https://github.com/dicodingacademy/assets/releases/download/release/rockpaperscissors.zip

"""Mengekstrak file zip"""

import zipfile,os
local_zip = '/content/rockpaperscissors.zip'
zip_ref = zipfile.ZipFile(local_zip, 'r')
zip_ref.extractall('/content/')
zip_ref.close()

"""Cek folder dalam content"""

os.listdir('/content/rockpaperscissors/rps-cv-images/')

base_dir = '/content/rockpaperscissors/rps-cv-images/'

"""import modul yang digunakan"""

import tensorflow as tf
import keras_preprocessing
from keras_preprocessing import image
from keras_preprocessing.image import ImageDataGenerator

"""Augmentasi & Pemisahan Data menjadi Training dan Validation"""

train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    horizontal_flip=True,
    shear_range = 0.2,
    fill_mode = 'nearest',
    validation_split = 0.4
)

train_generator = train_datagen.flow_from_directory(
    base_dir,
    target_size=(100,150),
    class_mode='categorical',
    subset='training'
)

validation_generator = train_datagen.flow_from_directory(
    base_dir,
    target_size=(100,150),
    class_mode='categorical',
    subset='validation'
)

"""Membangun Model Sequential Jaringan Saraf Tiruan"""

model = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(32, (3,3), activation='relu', input_shape=(100, 150, 3)), 
    tf.keras.layers.MaxPooling2D(2, 2),
    tf.keras.layers.Conv2D(64, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),
    tf.keras.layers.Conv2D(128, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),
    tf.keras.layers.Conv2D(256, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(512, activation='relu'),
    tf.keras.layers.Dense(3, activation='softmax')
])

model.summary()

"""Kompilasi model"""

model.compile(
    loss='categorical_crossentropy',
    optimizer=tf.optimizers.Adam(),
    metrics=['accuracy'])

"""Melatih model"""

model.fit(
    train_generator,
    epochs=20,
    steps_per_epoch=20,
    validation_data=validation_generator,
    validation_steps=5,
    verbose=2
)

"""Uji coba model"""

import numpy as np
from google.colab import files
import matplotlib.pyplot as plt

uploaded = files.upload()
for fn in uploaded.keys():
  path = fn
  img = tf.keras.utils.load_img(path, target_size=(100, 150))
  imgplot = plt.imshow(img)
  x = image.img_to_array(img)
  x = np.expand_dims(x, axis=0)
  images = np.vstack([x])
  classes = model.predict(images, batch_size=10)
  print(fn)
  if classes[0][0]==1:
    print('bentuk kertas')
  elif classes[0][1]==1:
    print('bentuk batu')
  elif classes[0][2]==1:
    print('bentuk gunting')
  else:
    print('tidak diketahui')