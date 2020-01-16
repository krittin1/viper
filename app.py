# requests are objects that flask handle
import sys
import os
import glob
import re
import numpy as np

import tensorflow as tf

from keras.applications.imagenet_utils import preprocess_input, decode_predictions
from keras.models import load_model
from keras.preprocessing import image

from flask import Flask, render_template, request, redirect, url_for, render_template

from werkzeug.utils import  secure_filename
from gevent.pywsgi import WSGIServer



# APP_ROOT = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)

MODEL_PATH = 'models/snake2.h5'

model = load_model(MODEL_PATH)
model._make_predict_function()          # Necessary

print('Model loading...')
from keras.applications.resnet50 import ResNet50
model = ResNet50(weights='imagenet')

graph = tf.get_default_graph()

print('Model loaded. Started serving...')

print('Model loaded. Check http://127.0.0.1:5000/')


def predictModel(img_path, model) :
    original = image.load_img(img_path, target_size=(224, 224))


    numpy_image = image.img_to_array(original)
    # todo:

    image_batch = np.expand_dims(numpy_image, axis=0)

    print('PIL image size = ', original.size)
    print('NumPy image size = ', numpy_image.shape)
    print('Batch image size = ', image_batch.shape)


    processed_image = preprocess_input(image_batch, mode = 'caffe')
    with graph.as_default():
        preds = model.predict(processed_image)




    print('Deleting File at Path: ' + img_path)

    os.remove(img_path)

    print('Deleting File at Path - Success - ')
    return preds


@app.route('/', defaults={'snake': ''}, methods=['GET', 'POST'])

def homepage(snake):
    return render_template('snake.html')



@app.route('/predict', methods=['GET', 'POST'])

def upload() :

    if request.method == 'POST':

        f = request.files['image']
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)
        print('Begin Model Prediction ...')

        preds = predictModel(file_path, model)

        print('End Model Prediction...')


        pred_class = decode_predictions(preds, top=1)
        result = str(pred_class[0][0][1])

        return result
    return None


if __name__=='__main__':
    app.debug = True;

    app.run();






if __name__ == "__main__":
    app.run(port=4555, debug=True)


