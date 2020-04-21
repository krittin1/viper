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
from importlib import reload

from flask import Flask, jsonify, request, render_template, session

from werkzeug.utils import secure_filename

# APP_ROOT = os.path.dirname(os.path.abspath(__file__))
# graph = tf.get_default_graph()
app = Flask(__name__)
MODEL_PATH = 'models/cobra2.h5'
GreenPit_PATH = 'models/GreenPitViper.h5'
KingCobra_PATH = 'models/kingcobra.h5'
russelViper_PATH = 'models/russelviper2.h5'
malayanviper_PATH = 'models/malayanviper.h5'
malayanKrait_PATH = 'models/malayanKrait.h5'
bandedKrait_PATH = 'models/banedKrait.h5'

model = load_model(MODEL_PATH)
greenPit = load_model(GreenPit_PATH)
KingCobra = load_model(KingCobra_PATH)
RusselViper = load_model(russelViper_PATH)
MalayanViper = load_model(malayanviper_PATH)
MalayanKrait = load_model(malayanKrait_PATH)
BandedKrait = load_model(bandedKrait_PATH)

BandedKrait._make_predict_function()
MalayanKrait._make_predict_function()
MalayanViper._make_predict_function()
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


    image_batch = np.expand_dims(numpy_image, axis=0)  ##ขยายเป้น numpy
    image_batch = image_batch / 255
    # print('PIL image size = ', original.size)
    # print('NumPy image size = ', numpy_image.shape)
    # print('Batch image size = ', image_batch.shape)

    # processed_image = preprocess_input(image_batch, mode = 'caffe')
    preds = model.predict(image_batch)

    return preds


@app.route('/content', methods=['GET', 'POST'])
def content():
    return render_template('content.html')

@app.route('/snake', methods=['GET', 'POST'])
def snake():
    return render_template('snake.html')

@app.route('/', defaults={'snake': ''}, methods=['GET', 'POST'])
def homepage(snake):
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':

        f = request.files['image']
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)
        print('Begin Model Prediction ...')



        snakeGroup = [model, greenPit, KingCobra, RusselViper,MalayanViper,MalayanKrait,BandedKrait]
        data = {"TH": [
            {
                "name": "งูเห่า",
                "accuracy": 1.0,
                "symptoms": "แสบบริเวณบาดแผล ปวดเล็กน้อย แขนขาจะไม่มีแรงและให้ความรู้สึกง่วงจนลืมตาไม่ขึ้น",
                "aid": "ควรรีบมาโรงพยาบาลโดยเร็วที่สุด และขยับส่วนที่ถูกกัดให้น้อยเฉพาะเท่าที่จำเป็น เพื่อลดการดูดซึมพิษงูที่สำคัญ ถ้าถูกงูเห่าพ่นพิษเข้าตา ควรล้างตาด้วยน้ำสะอาดปริมาณมาก",
                "type": "มีพิษ",
                "colorStyle": "red"

            },
            {
                "name": "งูเขียวหางไหม้",
                "accuracy": 2.0,
                "symptoms": "ผิวหนังพองเป็นถุงน้ำ มีเลือดซึมออกจากแผลรอยเขี้ยวพบรอยเขียวช้ำ มีโอกาสทำให้เนื้อตาย อาจทำให้อาเจียนเป็นเลือดหรือปัสสาวะเป็นเลือด",
                "aid": "ขยับจุดที่โดนกัดให้น้อยที่สุด ควรทำความสะอาดแผลด้วยน้ำสะอาด หรือน้ำเกลือล้างแผล รีบไปพบแพทย์เพื่อทำการรักษาตั้งแต่เบื้องต้น ไม่ควรรักษาเอง **ห้ามใช้ปากดูดพิษเด็ดขาด**",
                "type": "มีพิษ",
                "colorStyle": "red"

            },
            {
                "name": "งูจงอาง",
                "accuracy": 3.0,
                "symptoms": "แสบบริเวณบาดแผล ปวดเล็กน้อย ทำให้กล้ามเนื้ออ่อนแรง หนังตาตก ทำให้มักเข้าใจผิดว่าผู้ป่วยง่วงนอน ต่อมาอาจมีกลืนลำบาก และเกิดอัมพาต",
                "aid": "ควรรีบมาโรงพยาบาลโดยเร็วที่สุด และขยับส่วนที่ถูกกัดให้น้อยเฉพาะเท่าที่จำเป็น เพื่อลดการดูดซึมพิษงู ไม่แนะนำให้ขันชะเนาะ ทำความสะอาดบาดแผลเพื่อลดการติดเชื้อ",
                "type": "มีพิษ",
                "colorStyle": "red"

            },
            {
                "name": "งูแมวเซา",
                "accuracy": 4.0,
                "symptoms": "เกิดอาการปวดและมีอาการบวมมาก เลือดออกตามไรฟันหรือไอมีเสมหะปนเลือด ถ่ายอุจาระสีดำปัสสาวะเป็นเลือด มีเลือดออกและการเแข็งตัวของเลือดผิดปกติ อาจทำให้ไตวายเฉียบพลัน",
                "aid": "ควรรีบมาโรงพยาบาลโดยเร็วที่สุด และขยับส่วนที่ถูกกัดให้น้อยเฉพาะเท่าที่จำเป็น เพื่อลดการดูดซึมพิษงู **ห้ามใช้ปากดูดพิษเด็ดขาด**",
                "type": "มีพิษ",
                "colorStyle": "red"

            },
            {
                "name": "งูกะปะ",
                "accuracy": 5.0,
                "symptoms": "จะพบตุ่มน้ำเลือดหลายอัน และบางอันมีขนาดใหญ่ และมีเลือดออกจากแผลที่ถูกกัด เลือดออกตามไรฟันหรือไอมีเสมหะปนเลือด ถ่ายอุจาระสีดำปัสสาวะเป็นเลือด มีเลือดออกและการเแข็งตัวของเลือดผิดปกติ",
                "aid": "ควรรีบมาโรงพยาบาลโดยเร็วที่สุด และขยับส่วนที่ถูกกัดให้น้อยเฉพาะเท่าที่จำเป็น เพื่อลดการดูดซึมพิษงู **ห้ามใช้ปากดูดพิษเด็ดขาด**",
                "type": "มีพิษ",
                "colorStyle": "red"

            },
            {
                "name": "งูทับสมิงคลา",
                "accuracy": 6.0,
                "symptoms": "มีอาการหนักที่หนังตาบน ตาพร่า ต่อมาจะพบหนังตาตก ลืมตาไม่ขึ้น ตากลอกไปมาไม่ได้",
                "aid": "ควรรีบมาโรงพยาบาลโดยเร็วที่สุด และขยับส่วนที่ถูกกัดให้น้อยเฉพาะเท่าที่จำเป็น เพื่อลดการดูดซึมพิษงู **ห้ามใช้ปากดูดพิษเด็ดขาด**",
                "type": "มีพิษ",
                "colorStyle": "red"
            },
            {
                "name": "งูสามเหลี่ยม",
                "accuracy": 7.0,
                "symptoms": "มีอาการหนักที่หนังตาบน ตาพร่า ต่อมาจะพบหนังตาตก ลืมตาไม่ขึ้น ตากลอกไปมาไม่ได้",
                "aid": "ควรรีบมาโรงพยาบาลโดยเร็วที่สุด และขยับส่วนที่ถูกกัดให้น้อยเฉพาะเท่าที่จำเป็น เพื่อลดการดูดซึมพิษงู **ห้ามใช้ปากดูดพิษเด็ดขาด**",
                "type": "มีพิษ",
                "colorStyle": "red"
            }
        ],
            "EN": [
                {
                    "name": "Cobra",
                    "accuracy": 1.0,
                    "symptoms": "pain&nbsp;at&nbsp;the&nbsp;bite&nbsp;site tiredness&nbsp;or&nbsp;muscle&nbsp;weakness weakness",
                    "aid": "Should hurry to the hospital as soon as possible And move the bitten part to as little as necessary To reduce the absorption of significant snake venom If the cobra was poisoned into the eyes Should wash eyes with plenty of water.",
                    "type": "Venomous",
                    "colorStyle": "red"

                },
                {
                    "name": "GreenPitViper",
                    "accuracy": 2.0,
                    "symptoms": "Bruising&nbsp;of&nbsp;the&nbsp;skin blood&nbsp;in&nbsp;your&nbsp;urine Swelling&nbsp;in&nbsp;lymph&nbsp;nodes&nbsp;near&nbsp;the&nbsp;bite",
                    "aid": "Should clean the wound with clean water Or saline Hurry to see a doctor for treatment from the beginning. Should not cure by yourself ** Do not use the mouth to suck venom at all **",
                    "type": "Venomous",
                    "colorStyle": "red"

                },
                {
                    "name": "KingCobra",
                    "accuracy": 3.0,
                    "symptoms": "Drowsiness Hyporeflexia Ophthalmoplegia",
                    "aid": "call emergency medical personnel to have them pick up and transport to hospital avoid sucking wound with mouth keep the limb as immobile as possible clean the wound with clean water Or saline not alcohol",
                    "type": "Venomous",
                    "colorStyle": "red"

                },
                {
                    "name": "Russel viper",
                    "accuracy": 4.0,
                    "symptoms": "blood&nbsp;in&nbsp;your&nbsp;urine Local&nbsp;pain&nbsp;at&nbsp;bite&nbsp;site Vomiting Hypotension Bleeding&nbsp;gums acute&nbsp;kidney&nbsp;failure",
                    "aid": "Should hurry to the hospital as soon as possible And move the bitten part to as little as necessary To reduce the absorption of snake venom ** Do not use the mouth to suck venom at all **",
                    "type": "Venomous",
                    "colorStyle": "red"

                },
                {
                    "name": "Malayan viper",
                    "accuracy": 5.0,
                    "symptoms": "local&nbsp;pain bruising inflammation blood&nbsp;in&nbsp;your&nbsp;urine Bleeding&nbsp;gums",
                    "aid": "Should hurry to the hospital as soon as possible And move the bitten part to as little as necessary To reduce the absorption of snake venom ** Do not use the mouth to suck venom at all **",
                    "type": "Venomous",
                    "colorStyle": "red"

                },
                {
                    "name": "Malayan Krait",
                    "accuracy": 6.0,
                    "symptoms": "Heavy&nbsp;on&nbsp;the&nbsp;upper&nbsp;eyelid blurred&nbsp;vision the&nbsp;eyelids&nbsp;could&nbsp;not&nbsp;open.",
                    "aid": "Should hurry to the hospital as soon as possible And move the bitten part to as little as necessary To reduce the absorption of snake venom   ** Do not use the mouth to suck venom at all **",
                    "type": "Venomous",
                    "colorStyle": "red"
                },
                {
                    "name": "Banded Krait",
                    "accuracy": 7.0,
                    "symptoms": "Heavy&nbsp;on&nbsp;the&nbsp;upper&nbsp;eyelid blurred&nbsp;vision the&nbsp;eyelids&nbsp;could&nbsp;not&nbsp;open.",
                    "aid": "Should hurry to the hospital as soon as possible And move the bitten part to as little as necessary To reduce the absorption of snake venom   **Do not use the mouth to suck venom at all **",
                    "type": "Venomous",
                    "colorStyle": "red"
                }
            ]
        }
        count = 0


        for i in data:
            for j in data[i]:
                preds = predictModel(file_path, snakeGroup[count])
                # percent = preds.item(0) * 100
                percent = (((preds.item(0) * 100) * 100) // 1) / 100
                j['accuracy'] = percent
                # data[count]['accuracy'] = percent
                count = count + 1
            count = 0

        snake_json = json.dumps(data, ensure_ascii=False)
        snake_json = json.loads(snake_json)  # แปลงเป็น object


        print('Deleting File at Path: ' + file_path)

        print('Deleting File at Path - Success - ')
        os.remove(file_path)


    print('End Model Prediction...')
    return jsonify(snake_json)

if __name__ == '__main__':
    app.debug = True
    app.run()