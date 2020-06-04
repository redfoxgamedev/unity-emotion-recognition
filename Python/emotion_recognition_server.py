from tensorflow import keras
from tensorflow.keras.models import load_model

import cv2
import os
import json, argparse, time
import numpy as np 
from time import sleep 
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.preprocessing.image import ImageDataGenerator

import another_model

from flask import Flask, request
from flask_cors import CORS

import PIL
from PIL import Image

app = Flask(__name__)
cors = CORS(app)
@app.route("/api/predict", methods=['POST'])
def predict():
    start = time.time()

    data = request.data.decode("utf-8")
    if data == "":
        params = request.form
        imagePixels = json.loads(params['imageData'])
    else:
        params = json.loads(data)
        imagePixels = params['imageData']
    
    #feed in, get the answer
    #imageCv = Image.fromarray(image)
    #img_np = cv2.imdecode(image, cv2.IMREAD_COLOR)

    # array = np.array(image, dtype=np.uint8)
    # image = Image.fromarray(array)
    print (len(imagePixels))

    listRGB = list(zip(*[iter(imagePixels)]*4))
    print(len(listRGB))

    # image_out = Image.new(mode="RGBA", size = (640,480))
    # image_out.putdata(listRGB)

    image_out = np.array(listRGB[::-1], dtype=np.uint8).reshape(480,640,4)

    # print(image_out)

    # image = Image.fromarray(image_out)
    # image.save('test.png')


    rect, face, image = face_detector(image_out)
    if np.sum([face]) != 0.0:
        roi = face.astype("float") / 255.0
        roi = img_to_array(roi)
        roi = np.expand_dims(roi, axis=0)

        #prediction
        #emotion prediction...
        preds = classifier.predict(roi)[0]
        label = class_labels[preds.argmax()]
    else:
        label = "none"

    json_data = json.dumps({'emotion':label})
    print("Time spent handling the request: %f" % (time.time() - start))
    return json_data


if __name__ == "__main__":
    print("Entering main program")

    #classifier = load_model("model_v6_23.hdf5")
    classifier = another_model.getAnotherModel()
    validation_data_dir = './fer2013/validation'

    class_labels = {0: "Angry", 1: "Disgusted", 2: "Fearful", 3: "Happy", 4: "Neutral", 5: "Sad", 6: "Surprised"}
    print(class_labels)

    face_classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    def face_detector(img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)
        faces = face_classifier.detectMultiScale(gray, 1.3, 5)
        if faces is ():
            return (0,0,0,0), np.zeros((48,48), np.uint8), img

        for (x,y,w,h) in faces:
            cv2.rectangle(img, (x,y), (x+w, y+h), (255,0,0), 2)
            roi_gray = gray[y:y+h, x:x+w]
        
        try:
            roi_gray = cv2.resize(roi_gray, (48, 48), interpolation = cv2.INTER_AREA)
        except:
            return (x, w, y, h), np.zeros((48,48), np.uint8), img
        return (x,w,y,h), roi_gray, img

    # cap = cv2.VideoCapture(0)

    # while True:
    #     ret, frame = cap.read()
    #     rect, face, image = face_detector(frame)
    #     if np.sum([face]) != 0.0:
    #         roi = face.astype("float") / 255.0
    #         roi = img_to_array(roi)
    #         roi = np.expand_dims(roi, axis=0)

    #         #prediction
    #         #emotion prediction...
    #         preds = classifier.predict(roi)[0]
    #         label = class_labels[preds.argmax()]
    #         label_position = (rect[0] + int((rect[1]/2)), rect[2]+25)
    #         cv2.putText(image, label, label_position, cv2.FONT_HERSHEY_SIMPLEX, 2, (0,255,0), 3)

    #     else:
    #             cv2.putText(image, "No Face Found", (20,60), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,255,0), 3)
        
    #     cv2.imshow('All', image)
    #     if cv2.waitKey(1) ==13:
    #         break

    # cap.release()
    # cv2.destroyAllWindows()
    
    print('Starting the API')
    app.run()