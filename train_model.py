import cv2
import os
import numpy as np
import pickle
from imutils import paths
from sklearn.preprocessing import LabelBinarizer
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Flatten, Dense
from helpers import resize_to_fit


data = []
labels = []
base_folder_img = "caractere_base"

img = paths.list_images(base_folder_img)


for file in img:
    label = file.split(os.path.sep)[-2]
    img = cv2.imread(file)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # PADRONIZAR A IMG EM 20X20

    img = resize_to_fit(img, 20, 20)

    # adicionar dimensão para o keras poder ler a img

    img = np.expand_dims(img, axis=2)

    # adicionar as listas de dados e rotulos

    labels.append(label)
    data.append(img)


data = np.array(data, dtype="float") / 255
labels = np.array(labels)

# separação em dados de treino (75%) e dados de teste (25%)

(X_train, X_test, Y_train, Y_test) = train_test_split(data, labels, test_size=0.25, random_state=0)


# Converter com one-hot encoding

lb = LabelBinarizer().fit(Y_train)
Y_train = lb.transform(Y_train)
Y_test = lb.transform(Y_test)


with open('labels_model.dat', 'wb') as file_pickle:
    pickle.dump(lb, file_pickle)

# criar e treinar a inteligência artificial

model = Sequential()

model.add(Conv2D(20, (5, 5), padding="same", input_shape=(20, 20, 1), activation="relu"))
model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))


# criar a 2 camada

model.add(Conv2D(50, (5, 5), padding="same", activation="relu"))
model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))

# mais uma camada

model.add(Flatten())
model.add(Dense(500, activation="relu"))


# camada de saida

model.add(Dense(33, activation="softmax"))

# compilar todas as camadas

model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])


# treinar a inteligencia artificial

model.fit(X_train, Y_train, validation_data=(X_test, Y_test), batch_size=33, epochs=10, verbose=1)


# salvar o modelo de um arquivo


model.save("trained_model.hdf5")