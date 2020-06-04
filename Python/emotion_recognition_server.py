import cv2
import os
import json, argparse, time
import numpy as np 
from time import sleep 
from tensorflow import keras
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from flask import Flask, request
from flask_cors import CORS

#this is link to another script containing definition of another model
import atulapra_model_definition as atulapra_model

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

    #transforms image from Unity into array with 4-tuples in it
    listRGB = list(zip(*[iter(imagePixels)]*4))

    #transforms the array into the image that OpenCV can read
    image_out = np.array(listRGB[::-1], dtype=np.uint8).reshape(480,640,4)

    #face detection
    rect, face, image = face_detector(image_out)

    if np.sum([face]) != 0.0:
        roi = face.astype("float") / 255.0
        roi = img_to_array(roi)
        roi = np.expand_dims(roi, axis=0)

        #emotion prediction
        preds = classifier.predict(roi)[0]
        label = class_labels[preds.argmax()]
    else:
        label = "none"

    json_data = json.dumps({'emotion':label})
    print("Time spent handling the request: %f" % (time.time() - start))
    return json_data


if __name__ == "__main__":
    print("Entering main program")

    #model used originally in the tutorial
    #classifier = load_model("model_v6_23.hdf5")

    #model used by another source, but which provides better results
    #comment this out and uncomment previous model to see the results
    classifier = atulapra_model.getAtulapraModel()

    class_labels = {0: "Angry", 1: "Disgusted", 2: "Fearful", 3: "Happy", 4: "Neutral", 5: "Sad", 6: "Surprised"}
    face_classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    #Face detection routine
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

    #starts the server on http://127.0.0.1:5000/
    print('Starting the API')
    app.run()