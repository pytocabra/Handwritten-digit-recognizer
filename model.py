import numpy as np
import tensorflow as tf 


mnist = tf.keras.datasets.mnist
(x_train, y_train), (x_test, y_test) = mnist.load_data()
# validation_data = list(zip(x_train, y_train))

# normalize data
x_train = x_train / 255.0


model = tf.keras.models.Sequential([
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(784, activation='relu'),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(10, activation='softmax')
])

model.compile(optimizer='adam',
            loss='sparse_categorical_crossentropy',metrics=['accuracy'])

model.fit(x_train, y_train, batch_size=32, validation_split=0.15, epochs=8)

model.save('saved_model/')
