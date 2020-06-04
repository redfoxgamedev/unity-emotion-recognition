# Visual Output for Emotion Recognition using Unity

## Disclaimer

This is by no means the final state of the project, rather a prototype showcasing what’s possible. This is probably one of the most crude, hacked together things you will ever see. Do not judge the code quality but rather what the prototype implies.

## Functionality overview

Unity captures the information from the web camera, sends the information to the local Python server operating on Flask, which processes the image and predicts and emotion and then sends the prediction back to Unity with Unity playing corresponding Particle Effect according to emotion received.
Python does all the “AI” work in this case with Unity just supplying the webcam data. In the current setup, since both run on the local machine, Python could in fact tackle even the web camera feed, letting Unity just display graphics.

## Issues
There are performance hiccups within Unity, related to the transformation of the webcam image and sending it to the server. Also, the entire process takes a bit of time since this doesn’t happen on a single thread within Unity but rather asynchronously.

## Next steps
- We would probably refine the Python layer: can use inter-process communication which should be much faster. Taking webcam processing to Python. 
- Different direction: Need to also look into taking image processing inside Unity (both face detection and emotion recognition), which would require building native libraries for OpenCV and Keras for C# and Unity.

## Technical details

### Python

#### Requirements

* Used Python 3.7.7 and pip3 v. 20.1.1
* Tensorflow v. 2.1.1. Install via pip3 install tensorflow. Needed for running pre-trained models.
* Additional libraries needed to run the server (all can be installed by pip3 install NAME_OF_LIBRARY)
    * tensorflow (training models and running pre-trained models)
    * opencv-python (computer vision for detecting faces)
    * numpy (operations on arrays)
    * Flask (creating server API)

#### Research and functionality

Python part was constructed by following certain parts of this [tutorial](https://towardsdatascience.com/face-detection-recognition-and-emotion-detection-in-8-lines-of-code-b2ce32d4d5de) and their corresponding [repository] (https://github.com/priya-dwivedi/face_and_emotion_detection). The most useful step-by-step code elaboration of their implementation along with other useful things is contained [here] (https://github.com/priya-dwivedi/face_and_emotion_detection/blob/master/src/EmotionDetector_v2.ipynb)

The model the tutorial provided did not work well for me. I searched the net and found a better one, linked on this [GitHub by atulapra] (https://github.com/atulapra/Emotion-detection). The direct link to download the model is [here](https://drive.google.com/file/d/1FUn0XNOzf-nQV7QjbBPA6-8GLoHNNgv-/view?usp=sharing). I included it here along with Python source code.

#### Running

To run the Python server (the essential part of this prototype), you need to navigate to the directory with the .py file and run python3 emotion_recognition_server.py. The server will start on http://127.0.0.1:5000/ and then Unity will be able to send the requests.

### Unity

#### Requirements

* Used Unity 2019.3.14f1. It is imperative that you also use the absolutely same version when running the Unity project from this repository. 

#### Functionality

In the MainScene you will find all the VFX used for triggering each and specific emotion and all the components performing logic attached on GameObjects. The most important component to explore would be the SendCameraFeed.cs. 
Webcam imagery is acquired by using WebcamTexture class. It is important to note that the image comes upside-down (at least in my case), and once the Python server receives it, it in fact flips it back to normal in order to process it correctly.

#### Running
Run from Editor (press Play). If the server is running too, soon enough the system will read the emotions and play corresponding particle effects.

## Support

Let me know whether there is something missing from this explanation.
