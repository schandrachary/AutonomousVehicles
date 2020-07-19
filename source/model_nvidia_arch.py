import csv
from scipy import ndimage
import numpy as np
import sklearn
import cv2
    
dirPath = 'ShivData'
lines = []
with open(dirPath+'/driving_log.csv') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for line in reader:
        lines.append(line)       

from sklearn.model_selection import train_test_split
train_samples, validation_samples = train_test_split(lines, test_size=0.2)

def generator(samples,  batch_size=32):
    num_samples = len(samples)
    while 1: # Loop forever so the generator never terminates
        sklearn.utils.shuffle(samples)
        for offset in range(0, num_samples, batch_size):
            batch_samples = samples[offset:offset+batch_size]

            images = []
            angles = []
            # create adjusted steering measurements for the side camera images
            correction = 0.2 # this is a parameter to tune            
            
            # process
            for batch_sample in batch_samples:
                centerName = dirPath+'/IMG/'+batch_sample[0].split('/')[-1]
                leftName = dirPath+'/IMG/'+batch_sample[1].split('/')[-1]
                rightName = dirPath+'/IMG/'+batch_sample[2].split('/')[-1]
                
                # Grab center image and its corresponding steering wheel angle
                center_image = ndimage.imread(centerName)
                center_angle = float(batch_sample[3])
                
                # Grab left image and compute its steering wheel angle
                left_image = ndimage.imread(leftName)
                left_angle = center_angle + correction
                
                # Grab right image and compute its steering wheel angle
                right_image = ndimage.imread(rightName)
                right_angle = center_angle - correction
                
                images.append(center_image)
                images.append(left_image)
                images.append(right_image)
                
                angles.append(center_angle)
                angles.append(left_angle)
                angles.append(right_angle)            
            
            
            # Store the images in a numpy array 
            X_train = np.array(images)
            y_train = np.array(angles)
            yield sklearn.utils.shuffle(X_train, y_train)
            
            
# Set our batch size
batch_size=128

# compile and train the model using the generator function
train_generator = generator(train_samples, batch_size=batch_size)
validation_generator = generator(validation_samples, batch_size=batch_size)

# Build a regression model
from keras.models import Sequential
from keras.layers import Flatten, Dense, Lambda, Activation, Cropping2D, Dropout
from keras.layers.convolutional import Conv2D
from keras.layers.pooling import MaxPooling2D
from math import ceil

model = Sequential()

# Preprocess - normalize and mean center the data
model.add(Lambda(lambda x: x/255.0 - 0.5, input_shape=(160,320,3)))

# Crop input images
model.add(Cropping2D(cropping=((50,25),(0,0))))

# Convolutional layer 1, subsample with 2x2 kernel
model.add(Conv2D(24, (5,5), activation='relu'))
model.add(MaxPooling2D((2,2)))

# Convolutional layer 2, subsample with 2x2 kernel
model.add(Conv2D(36, (5,5), activation='relu'))
model.add(MaxPooling2D((2,2)))

# Convolutional layer 3, subsample with 2x2 kernel
model.add(Conv2D(48, (5,5), activation='relu'))
model.add(MaxPooling2D((2,2)))

# Convolutional layer 4, no subsampling
model.add(Conv2D(64, (3,3), activation='relu'))

# Convolutional layer 5, no subsampling
model.add(Conv2D(64, (3,3), activation='relu'))

# Dropout layer - 1
model.add(Dropout(0.35))

# Flatten the layer
model.add(Flatten())

# Dropout layer - 2
# model.add(Dropout(0.45))

# Fully connected layer 1
model.add(Dense(100))#, activation='relu'))

# Dropout layer - 3
model.add(Dropout(0.50))

# Fully connected layer 2
model.add(Dense(50))#, activation='relu'))

# Dropout layer - 4
model.add(Dropout(0.50))

# Fully connected layer 3
model.add(Dense(10))#, activation='relu'))

# Fully connected layer 5
model.add(Dense(1))


# Compile the model with mse since its a regression model
model.compile(loss='mse', optimizer='adam')
# history_object = model.fit(X_train, y_train, validation_split=0.2, shuffle=True, verbose=1, nb_epoch=5)
history_object = model.fit_generator(train_generator, steps_per_epoch=ceil(len(train_samples)/batch_size), validation_data=validation_generator, \
                                     validation_steps=ceil(len(validation_samples)/batch_size), epochs=4, verbose=1)

# Save the model
model.save('model.h5')

### print the keys contained in the history object
print(history_object.history.keys())

import matplotlib.pyplot as plt

### plot the training and validation loss for each epoch
plt.plot(history_object.history['loss'])
plt.plot(history_object.history['val_loss'])
plt.title('model mean squared error loss')
plt.ylabel('mean squared error loss')
plt.xlabel('epoch')
plt.legend(['training set', 'validation set'], loc='upper right')
# plt.show()
plt.savefig('loss function.png')
exit()
