# import the necessary packages
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth.models import User
import base64
from PIL import Image
from io import StringIO
import numpy as np
import urllib.request
import json
import cv2
import os
import random
import uuid
from django.shortcuts import render, get_object_or_404, redirect

# define the path to the face detector and smile detector
FACE_DETECTOR_PATH = "{base_path}/cascades/haarcascade_frontalface_default.xml".format(
    base_path=os.path.abspath(os.path.dirname(__file__)))

SMILE_DETECTOR_PATH = "{base_path}/cascades/haarcascade_smile.xml".format(
    base_path=os.path.abspath(os.path.dirname(__file__)))

# path to trained faces and labels
TRAINED_FACES_PATH = "{base_path}/faces".format(
    base_path=os.path.abspath(os.path.dirname(__file__)))

# maximum distance between face and match
THRESHOLD = 75

# create the cascade classifiers
detector = cv2.CascadeClassifier(FACE_DETECTOR_PATH)
smiledetector = cv2.CascadeClassifier(SMILE_DETECTOR_PATH)


def get_images_and_labels(path):
    # images will contains face images
    images = []
    # labels will contains the label that is assigned to the image
    labels = []
    user_paths = [f for f in os.listdir(path) if not f.endswith('.DS_Store')]
    for user_path in user_paths:
        # Append all the absolute image paths in a list image_paths
        image_paths = [os.path.join(os.path.join(path, user_path), f) for f in os.listdir(os.path.join(path, user_path))
                       if not f.endswith('.DS_Store')]
        for image_path in image_paths:
            # Read the image and convert to grayscale
            image_pil = Image.open(image_path).convert('L')
            # Convert the image format into numpy array
            image = np.array(image_pil, 'uint8')
            # Detect the face in the image
            faces = detector.detectMultiScale(image)
            # If face is detected, append the face to images and the label to labels
            for (x, y, w, h) in faces:
                images.append(image[y: y + h, x: x + w])
                labels.append(int(user_path))
                # cv2.imshow("Adding faces to traning set...", image[y: y + h, x: x + w])
                # cv2.waitKey(50)
        # return the images list and labels list
    return images, labels


recognizer = cv2.face.LBPHFaceRecognizer_create()
images, labels = get_images_and_labels(TRAINED_FACES_PATH)
recognizer.train(images, np.array(labels))


@csrf_exempt
def recognize(request, img):
    img = img[22:]
    # initialize the data dictionary to be returned by the request
    data = {}
    # check to see if this is a get request
    if request.method == "GET":
        # check to see if an image was uploaded
        # if request.GET.get("imageBase64", None) is not None:
        # grab the uploaded image
        image = _grab_image(base64_string=img)

        # otherwise, assume that a URL was passed in

        # convert the image to grayscale, load the face cascade detector,
        # and detect faces in the image
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        rects = detector.detectMultiScale(image, scaleFactor=1.1, minNeighbors=5,
                                          minSize=(30, 30), flags=0)

        # construct a list of bounding boxes from the detection
        rects = [(int(x), int(y), int(x + w), int(y + h)) for (x, y, w, h) in rects]
        if len(rects) == 0:
            data.update({"detected": False})
        else:
            x, y, w, h = rects[0]
            recognizer.setThreshold(THRESHOLD)
            identity, confidence = recognizer.predict(
                cv2.resize(image[y:h, x:w], (256, 256))
            )
            smile = smiledetector.detectMultiScale(
                image[y:h, x:w],
                scaleFactor=1.7,
                minNeighbors=22,
                minSize=(25, 25),
                flags=0)
            smiling = False if len(smile) == 0 else True
            try:
                user = User.objects.get(id=identity)
                user = {
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "username": user.username,
                    "email": user.email,
                    "id": user.pk,
                }

            except  User.DoesNotExist:
                user = ""

            # update the data dictionary with the faces detected
            data.update({"detected": True, "identity": identity, "user": user, "box": rects, "smiling": smiling})

    if user is not "":
        r = redirect('manager:index')
        print('Bande khoda', user)
        r.set_cookie('permission', 'T')
        r.set_cookie('login_user', user)
        r.set_cookie('user', user['username'])

        # return a JSON response
        return r
    else:
        return redirect('image:image_login')


@csrf_exempt
def train(request, img):
    img = img[22:]
    name1 = request.COOKIES.get('user')
    user = User.objects.filter(first_name=name1)[0]
    if request.method == "GET":
        # check to see if an image was uploaded
        # if request.GET.get("imageBase64", None) is not None and request.GET.get("user", None) is not None:
        # grab the uploaded image
        image = _grab_image(base64_string=img)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        rects = detector.detectMultiScale(image, scaleFactor=1.1, minNeighbors=5,
                                          minSize=(30, 30), flags=0)

        # construct a list of bounding boxes from the detection
        rects = [(int(x), int(y), int(x + w), int(y + h)) for (x, y, w, h) in rects]
        if len(rects) == 0:
            return JsonResponse({"error": "No faces detected"})
        else:
            x, y, w, h = rects[0]
            cv2.imwrite(
                TRAINED_FACES_PATH + "/" + str(user.pk) + "/" + str(uuid.uuid4()) + ".jpg",
                cv2.resize(image[y:h, x:w], (256, 256)));
    return redirect('image:image_save')


@csrf_exempt
def new(request):
    if request.method == "GET":
        name1 = request.COOKIES.get('user')
        # if request.GET.get("username", None) is not None and request.GET.get("email", None) is not None:
        user = User.objects.create_user(name1, '')
        user.first_name = name1
        user.last_name = name1
        user.save()
        training_folder = os.path.join(TRAINED_FACES_PATH, str(user.pk))
        if not os.path.exists(training_folder):
            os.makedirs(training_folder)
    return redirect('manager:index')


@csrf_exempt
def users(request):
    users = [{"first_name": user.first_name, "last_name": user.last_name, "id": user.pk} for user in User.objects.all()]

    return JsonResponse({"users": users})


def _grab_image(path=None, base64_string=None, url=None):
    # if the path is not None, then load the image from disk
    if path is not None:
        image = cv2.imread(path)

    # otherwise, the image does not reside on disk
    else:
        # if the URL is not None, then download the image
        if url is not None:
            with urllib.request.urlopen(url) as resp:
                data = resp.read()
                image = np.asarray(bytearray(data), dtype="uint8")
                image = cv2.imdecode(image, cv2.IMREAD_COLOR)

        # if the stream is not None, then the image has been uploaded
        elif base64_string is not None:
            # sbuf = StringIO()
            # sbuf.write(base64.b64decode(base64_string))
            # pimg = Image.open(sbuf)
            # image = cv2.cvtColor(np.array(pimg), cv2.COLOR_RGB2BGR)

            image = base64.b64decode(base64_string)
            image = np.fromstring(image, dtype=np.uint8)
            image = cv2.imdecode(image, 1)

    # convert the image to a NumPy array and then read it into
    # OpenCV format

    # return the image
    return image
