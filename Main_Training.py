from sklearn.datasets import load_files
from tensorflow.keras.utils import to_categorical
import numpy as np
from glob import glob

from tensorflow.keras.preprocessing import image
from tqdm import tqdm
from PIL import ImageFile
import matplotlib.pyplot as plt

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout, Activation
from tensorflow.keras import optimizers

# -------------------- Config --------------------
tar = 15                        # number of classes
path = './dataset/'
img_width, img_height = 224, 224
epoch = 5
batch_size = 32
nb_filters1 = 32
nb_filters2 = 64
conv1_size = 3
conv2_size = 3
pool_size = 3
lr = 0.0004

# -------------------- Data loading --------------------
def load_dataset(path):
    data = load_files(path)
    files = np.array(data['filenames'])
    targets = to_categorical(np.array(data['target']), tar)
    return files, targets

train_files, train_targets = load_dataset(path)
test_files = train_files
test_targets = train_targets

# (Optional) class names, not used later
burn_classes = [item[10:-1] for item in sorted(glob("./dataset/*/"))]

# -------------------- Image -> tensor helpers --------------------
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

def path_to_tensor(img_path, width=img_width, height=img_height):
    img = image.load_img(img_path, target_size=(width, height))
    x = image.img_to_array(img)
    return np.expand_dims(x, axis=0)

def paths_to_tensor(img_paths, width=img_width, height=img_height):
    list_of_tensors = [path_to_tensor(p, width, height) for p in tqdm(img_paths)]
    return np.vstack(list_of_tensors)

# Preprocess
train_tensors = paths_to_tensor(train_files).astype('float32') / 255.0
test_tensors  = paths_to_tensor(test_files ).astype('float32') / 255.0

# -------------------- Model --------------------
model = Sequential()
model.add(Conv2D(nb_filters1, (conv1_size, conv1_size), padding='same',
                 input_shape=(img_width, img_height, 3)))
model.add(Activation("relu"))
model.add(MaxPooling2D(pool_size=(pool_size, pool_size)))

model.add(Conv2D(nb_filters2, (conv2_size, conv2_size), padding='same'))
model.add(Activation("relu"))
model.add(MaxPooling2D(pool_size=(pool_size, pool_size)))

model.add(Flatten())
model.add(Dense(256))
model.add(Activation("relu"))
model.add(Dropout(0.5))
model.add(Dense(tar, activation='softmax'))

model.compile(
    loss='categorical_crossentropy',
    optimizer=optimizers.RMSprop(learning_rate=lr),
    metrics=['accuracy']
)

# -------------------- Train --------------------
history = model.fit(
    train_tensors, train_targets,
    validation_split=0.30,
    epochs=epoch,
    batch_size=10,
    shuffle=True
)

# -------------------- Plot --------------------
def show_history_graph(history):
    plt.figure()
    plt.plot(history.history['accuracy'])
    plt.plot(history.history['val_accuracy'])
    plt.title('model accuracy')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['train', 'validation'], loc='upper left')
    plt.show()

show_history_graph(history)

# -------------------- Save --------------------
model.save('CNN2D.h5')
