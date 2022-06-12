import sys
sys.path.append(".")
from PIL import Image
from common.functions import sigmoid, softmax
from dataset.mnist import load_mnist
import pickle
import numpy as np
import os


def get_data():
    (x_train, t_train), (x_test, t_test) = load_mnist(
        normalize=True, flatten=True, one_hot_label=False)
    return x_test, t_test


def init_network():
    with open("recognize_panel/data/sample_weight.pkl", 'rb') as f:
        network = pickle.load(f)
    return network


def predict(network, x):
    W1, W2, W3 = network['W1'], network['W2'], network['W3']
    b1, b2, b3 = network['b1'], network['b2'], network['b3']

    a1 = np.dot(x, W1) + b1
    z1 = sigmoid(a1)
    a2 = np.dot(z1, W2) + b2
    z2 = sigmoid(a2)
    a3 = np.dot(z2, W3) + b3
    y = softmax(a3)

    return y


def recognize(img_path):
    img = Image.open(img_path)
    img = img.resize((28, 28), Image.ANTIALIAS).convert("L")
    img.save(img_path)

    img = np.asarray(img, dtype=np.uint8)
    # print(img.shape)
    

    # pil_img = Image.fromarray(img)
    # pil_img.show()
    img_data = img.reshape(28*28, ) / 255.0
    # print(img_data)

    network = init_network()
    y = predict(network, img_data)
    return np.argmax(y)


# recognize("./recognize_panel/data/digit.png")