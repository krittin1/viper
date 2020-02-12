# requests are objects that flask handle
import sys
import os
import re
import numpy as np
import operator
import tensorflow as tf
import json
from keras.applications.imagenet_utils import preprocess_input, decode_predictions
from keras.models import load_model
from keras.preprocessing import image

from flask import Flask, jsonify, render_template, request, redirect, url_for, render_template

from werkzeug.utils import secure_filename

# APP_ROOT = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)

MODEL_PATH = 'models/cobra2.h5'
GreenPit_PATH = 'models/GreenPitViper.h5'
KingCobra_PATH = 'models/kingcobra.h5'
russelViper_PATH = 'models/russelviper2.h5'
model = load_model(MODEL_PATH)
greenPit = load_model(GreenPit_PATH)
KingCobra = load_model(KingCobra_PATH)
RusselViper = load_model(russelViper_PATH)
RusselViper._make_predict_function()
KingCobra._make_predict_function()

greenPit._make_predict_function()

model._make_predict_function()  # Necessary

print('Model loading...')

print('Model loaded. Started serving...')

print('Model loaded. Check http://127.0.0.1:5000/')


def predictModel(img_path, model):
    original = image.load_img(img_path, target_size=(64, 64))

    numpy_image = image.img_to_array(original)
    # todo:

    image_batch = np.expand_dims(numpy_image, axis=0)  ##ขยายเป้น numpy
    image_batch = image_batch / 255
    print('PIL image size = ', original.size)
    print('NumPy image size = ', numpy_image.shape)
    print('Batch image size = ', image_batch.shape)

    # processed_image = preprocess_input(image_batch, mode = 'caffe')
    preds = model.predict(image_batch)

    return preds


@app.route('/content', methods=['GET', 'POST'])
def content():
    return render_template('content.html')


@app.route('/', defaults={'snake': ''}, methods=['GET', 'POST'])
def homepage(snake):
    return render_template('snake.html')


@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':

        f = request.files['image']
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)
        print('Begin Model Prediction ...')

        # preds = predictModel(file_path, model)
        # green = predictModel(file_path,greenPit)

        snakeGroup = [model, greenPit, KingCobra, RusselViper]
        data = [{
            "name": "งูเห่า",
            "accuracy": 1.0,
            "symptoms": "หากโดนกัดจะมีอาการแสบบริเวณบาดแผล ต่อมาจะมีอาการปวดเล็กน้อย ผ่านไป สามสิบนาที จะมีอาการปวดรอบบาดแผลและบวมมากขึ้น ในเวลาต่อมาแขนและขาจะไม่มีแรง ให้ความรุ้สึกง่วงซึมจนลืมตาไม่ขึ้น",
            "aid": "ควรรีบพบแพทย์โดยเร็วที่สุดและขยับส่วนที่ถูกกัดให้น้อยเฉพาะเท่าที่จำเป็น เพื่อลดการดูดซึมพิษงูที่สำคัญ ถ้าถูกงูเห่าพ่นพิษเข้าตา ควรล้างตาด้วยน้ำสะอาดปริมาณมาก **ห้ามใช้ปากดูดพิษเด็ดขาด**",
            "type": "มีพิษ",
            "colorStyle": "red"

        },
            {
                "name": "งูเขียวหางไหม้",
                "accuracy": 2.0,
                "symptoms": "มีอาการเฉพาะที่ ปวดบวมชัดเจน ตั้งแต่น้อยจนถึงมาก อาจพบผิวหนังพองเป็นถุงน้ำ หรือมีเลือดซึมออกจากแผลรอยเขี้ยว บางรายอาจพบเนื้อตายร่วมด้วย อาการทั่วไป เลือดออกผิดปกติตามอวัยวะต่างๆ ทั่วร่างกาย ได้แก่ เลือดออกตามไรฟัน ลือดออกตามรอยแผลเขี้ยวที่ถูกกัดและรอยเขียวช้ำ อาจมีเลือดออกในกล้ามเนื้อ อาเจียนเป็นเลือด หรือปัสสาวะเป็นเลือด เป็นต้น",
                "aid": " มีการขยับน้อยที่สุด ควรทำความสะอาดแผลด้วยน้ำสะอาด หรือน้ำเกลือล้างแผล รีบไปพบแพทย์เพื่อทำการรักษาตั้งแต่เบื้องต้น ไม่ควรรักษาเอง **ห้ามใช้ปากดูดพิษเด็ดขาด**",
                "type": "มีพิษ",
                "colorStyle": "red"

            },
            {
                "name": "งูจงอาง",
                "accuracy": 3.0,
                "symptoms": "อาการ",
                "aid": "ปฐมพยาบาลเบื้องต้น",
                "type": "มีพิษ",
                "colorStyle": "red"

            },
            {
                "name": "งูแมวเซา",
                "accuracy": 4.0,
                "symptoms": "มีการขยับน้อยที่สุด ควรทำความสะอาดแผลด้วยน้ำสะอาด หรือน้ำเกลือล้างแผล รีบไปพบแพทย์เพื่อทำการรักษาตั้งแต่เบื้องต้น ไม่ควรรักษาเอง **ห้ามใช้ปากดูดพิษเด็ดขาด**",
                "aid": "ควรรีบมาโรงพยาบาลโดยเร็วที่สุด และขยับส่วนที่ถูกกัดให้น้อยเฉพาะเท่าที่จำเป็น เพื่อลดการดูดซึมพิษงู **ห้ามใช้ปากดูดพิษเด็ดขาด**",
                "type": "มีพิษ",
                "colorStyle": "green"

            }]
        count = 0
        for i in data:
            preds = predictModel(file_path, snakeGroup[count])
            percent = preds.item(0) * 100
            percent = ((percent * 100) // 1) / 100
            data[count]["accuracy"] = percent
            count = count + 1

        # print(data)
        snake_json = json.dumps(data, ensure_ascii=False)
        snake_json = json.loads(snake_json)  # แปลงเป็น object

        print(snake_json)

        # accuracy = {k: v for k, v in sorted(accuracy.items(), key=lambda x: x[1])}
        # for i, j in accuracy.items():
        #     print(i, j)
        print('Deleting File at Path: ' + file_path)

        print('Deleting File at Path - Success - ')
        os.remove(file_path)

    print('End Model Prediction...')
    return jsonify(snake_json)


if __name__ == '__main__':
    app.debug = True;

    app.run();

# if __name__ == "__main__":
#     app.run(debug=True)
