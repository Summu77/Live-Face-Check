from flask import Flask, render_template, request, jsonify
import base64
import numpy as np
import cv2
from PIL import Image
from io import BytesIO
import torch
from API.tools import *

app = Flask(__name__)

def convert_to_dict(res):
    res_dict = {}
    for key, value in res.items():
        if isinstance(value, torch.Tensor):
            # 如果是 Tensor 对象，则转换为 Python 的列表
            res_dict[key] = value.tolist()
        else:
            res_dict[key] = value
    return res_dict

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/API_1', methods=['POST'])
def API_1(): 
    # save the img
    data = request.json['image']
    header, encoded = data.split(",", 1)
    binary = base64.b64decode(encoded)
    img_path = "/home/ns/Homework/Face/data/received_image.png"
    with open(img_path, "wb") as image_file:
        image_file.write(binary)
        
    # get results
    res = search_baidu(img_path)
    res['score'] = round(res['score'] / 100, 2)
    
    # pass or not
    if float(res['score']) > 0.6 and res['livepass'] == "PASS":
        res['pass'] = "PASS"
    else:
        res['unpass'] = "UNPASS"
    return jsonify(res)


@app.route('/API_2', methods=['POST'])
def API_2(): 
    # save the img
    data = request.json['image']
    header, encoded = data.split(",", 1)
    binary = base64.b64decode(encoded)
    img_path = "/home/ns/Homework/Face/data/received_image.png"
    with open(img_path, "wb") as image_file:
        image_file.write(binary)
    
    # get results
    res = search_face_recognition(img_path)
    res['score'] = round(res['score'], 2)
    res = gender_age_expression_live(img_path, res)
    
    # pass or not
    if float(res['score']) > 0.5 and res['livepass'] == "PASS":
        res['pass'] = "PASS"
    else:
        res['unpass'] = "UNPASS"
    
    res_dict = convert_to_dict(res)
    return jsonify(res_dict)


@app.route('/API_3', methods=['POST'])
def API_3():
    
    # save the img
    data = request.json['image']
    header, encoded = data.split(",", 1)
    binary = base64.b64decode(encoded)
    img_path = "/home/ns/Homework/Face/data/received_image.png"
    with open(img_path, "wb") as image_file:
        image_file.write(binary)
    
    # get results
    res = search_facenet(img_path)
    res['score'] = round(res['score'], 2)
    res = gender_age_expression_live(img_path, res)
    
    # pass or not
    if float(res['score']) > 0.5 and res['livepass'] == "PASS":
        res['pass'] = "PASS"
    else:
        res['unpass'] = "UNPASS"
    
    res_dict = convert_to_dict(res)
    return jsonify(res_dict)

if __name__ == '__main__':
    
    app.run(host='0.0.0.0', port=5000,  debug=True)
