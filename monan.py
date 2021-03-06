# -*- coding: utf-8 -*-
"""monan.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1VRfqmTeDfk0Q12MKcUTCZrqEDhPL3FLE
"""

from google.colab import drive
drive.mount("/content/drive")

import tensorflow as tf
from tensorflow import keras
from keras.models import Sequential
from keras.layers.convolutional import Conv2D
from keras.layers.convolutional import MaxPooling2D
from keras.layers import Flatten
from keras.layers import Dense, Dropout
from tensorflow.keras.preprocessing.image import ImageDataGenerator

#initialising the CNN
classifier = Sequential()
#step1 - Convolution
from keras.layers import Dense, Dropout
classifier.add(Conv2D(128, (3,3), activation='relu',kernel_initializer='he_uniform',padding='same',input_shape=(150,150,3)))
classifier.add(MaxPooling2D(pool_size =(2, 2)))
classifier.add(Conv2D(32, (3, 3), activation='relu',kernel_initializer='he_uniform',padding='same'))
classifier.add(MaxPooling2D(pool_size=(2, 2)))
classifier.add(Flatten())
classifier.add(Dense(units = 128, activation= 'relu',kernel_initializer = 'he_uniform'))
classifier.add(Dropout(0.2))
classifier.add(Dense(units = 10, activation = 'softmax')) #Bao nhiêu người thì units = x bấy nhiêu

#Compiling the CNN
classifier.compile(optimizer = 'adam', loss='categorical_crossentropy', metrics = ['accuracy'])

train_datagen = ImageDataGenerator(rescale=1./255,
                                   shear_range=0.2,
                                   zoom_range=0.2,
                                   horizontal_flip=True)
training_set=train_datagen.flow_from_directory('/content/drive/MyDrive/monan/train',
                                               target_size=(150,150),
                                               batch_size=32,
                                               class_mode ='categorical')
test_set=train_datagen.flow_from_directory('/content/drive/MyDrive/monan/test',
                                               target_size=(150,150),
                                               batch_size=32,
                                               class_mode ='categorical')

#from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint 
#callbacks = [EarlyStopping(monitor = 'val_loss', patience =100), ModelCheckpoint('model_checkpoint_new.h5', save_best_only True)] 
from tensorflow.keras.callbacks import EarlyStopping
classifier.compile(optimizer = 'adam', loss = 'categorical_crossentropy',metrics = ['accuracy'])
callbacks=[EarlyStopping(monitor='val_loss',patience=100)]

history=classifier.fit(training_set,
                  steps_per_epoch=len(training_set),
                  batch_size = 64,
                  epochs=30,
                  validation_data=test_set,
                  validation_steps=len(test_set),
                  callbacks=callbacks,
                  verbose = 1)

#đánh giá chất lượng của mô hình và vẽ lại
score = classifier.evaluate(test_set,verbose=0)
print('Sai số kiểm tra là: ',score[0])
print('Độ chính xác kiểm tra là: ',score[1])
print('Done Train')
classifier.save('classifier_VietNameseFOOD.h5')
print('Done Save')

#Test kiểm tra mô hình train
from tensorflow.keras.models import load_model
model=load_model('/content/classifier_VietNameseFOOD.h5')
from tensorflow.keras.utils import load_img
from tensorflow.keras.utils import img_to_array
test_img=load_img('/content/(1).jpg',target_size=(150,150))
import numpy as np
test_img= img_to_array(test_img)
test_img=test_img/255
test_img=np.expand_dims(test_img,axis=0)
result=model.predict(test_img)
if round(result[0][0])==1:
   prediction="BÁNH BAO"
elif round(result[0][1])==1:
   prediction="BÁNH MÌ"
elif round(result[0][2])==1:
   prediction="BÁNH TRÁNG NƯỚNG"  
elif round(result[0][3])==1:
   prediction="BÁNH TRƯNG"  
elif round(result[0][4])==1:
   prediction="BÁNH TRUNG THU"  
elif round(result[0][5])==1:
   prediction="BÁNH XÈO"  
elif round(result[0][6])==1:
   prediction="CHẢ GIÒ"  
elif round(result[0][7])==1:
   prediction="CƠM TẤM"  
elif round(result[0][8])==1:
   prediction="GỎI CUỐN"  
elif round(result[0][9])==1:
   prediction="PHỞ"  
else:
  prediction = " "
print('=====> ĐÂY LÀ MÓN: ' + prediction)