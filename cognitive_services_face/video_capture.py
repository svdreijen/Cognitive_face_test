# Import libraries
import numpy as np
import cv2
import matplotlib.patches as patches
import requests
import cognitive_face as CF
import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO
import azure.cognitiveservices.vision.face as face
from msrest.authentication import CognitiveServicesCredentials
import json

# Define the keys and api urls for face api
subscription_key_face = '6fa0509cc7a64886a6775e56ec98d763'
face_api_url = 'https://westeurope.api.cognitive.microsoft.com/face/v1.0/'

credentials = CognitiveServicesCredentials(subscription_key_face)
myface = face.FaceClient(face_api_url, credentials)

# Set the key and api url for the python face SDK
CF.Key.set(subscription_key_face)
CF.BaseUrl.set(face_api_url)

# Define the keys and api urls for vision api
subscription_key_vision = "4303a199f4c749bf911015d6dd999ae3"
vision_base_url = "https://westeurope.api.cognitive.microsoft.com/vision/v2.0/"
analyze_url = vision_base_url + "analyze"

# Define functions used later in script
# Get the coordinates of rectangle from face detect to draw box
def getRectangle(faceDictionary):
    rect = faceDictionary['faceRectangle']
    left = rect['left']
    top = rect['top']
    bottom = left + rect['height']
    right = top + rect['width']
    return ((left, top), (bottom, right))

# Get the coordinates of rectangle from object detection to draw box
def rectangler(object):
    rect = object['rectangle']
    top = rect['x']
    left = rect['y']
    bottom = left + rect['h']
    right = top + rect['w']
    return ((left, top), (bottom, right))

# Capture webcam stream and read out frame
cap = cv2.VideoCapture(0)
ret, frame = cap.read()

# Convert the frame numpy array to .jpg binary string
frame_str = cv2.imencode('.jpg', frame)[1].tostring()

# Our operations on the frame come here
#cv2.imwrite("frame.jpg", frame)
#img_url = r'frame.jpg'

# Detect the face in the picture
#face = CF.face.detect(img_url)

headers     = {'Ocp-Apim-Subscription-Key' : subscription_key_face,
                'Content-Type': 'application/octet-stream'}

params      = {'returnFaceLandmarks' : 'True'}

response = requests.post(
    face_api_url + "detect", headers=headers, params=params, data=frame_str)

response.raise_for_status()

analysis_face = response.json()
print(analysis_face)

# Verify if the detected face matches person database
headers     = {'Ocp-Apim-Subscription-Key' : subscription_key_face,
                'Content-Type' : 'application/json'}

data        = {'faceId' : analysis_face[0]['faceId'],
                'personId' : siem['personId'],
                'personGroupId': 'test'}

data = json.dumps(data)

response = requests.post(
    face_api_url + "verify", headers=headers, data=data)

response.raise_for_status()

analysis_verify = response.json()

# Detect object in the picture
#image_data = open(img_url, 'rb').read()
headers    = {'Ocp-Apim-Subscription-Key': subscription_key_vision,
              'Content-Type': 'application/octet-stream'}

params     = {'visualFeatures': 'Objects'}

response = requests.post(
    analyze_url, headers=headers, params=params, data=frame_str)

response.raise_for_status()

analysis = response.json()

if face:
    faces = CF.face.verify(analysis_face[0]['faceId'], person_group_id='test', person_id=siem['personId'])

#img = Image.open(img_url)
#draw = ImageDraw.Draw(img)
#draw.rectangle(getRectangle(face[0]), outline='red')
#draw.rectangle(rectangler(analysis['objects'][0]), outline='blue')

# Display the resulting frame


#if cv2.waitKey(1) & 0xFF == ord('q'):
#   break
# Create a Rectangle patch
rectangle = (analysis['objects'][0]['rectangle']['x'], analysis['objects'][0]['rectangle']['y'])
width = analysis['objects'][0]['rectangle']['w']
height = analysis['objects'][0]['rectangle']['h']
rect = patches.Rectangle(rectangle, width, height, linewidth=1,edgecolor='r',facecolor='none')

rectangle2 = (analysis_face[0]['faceRectangle']['left'], analysis_face[0]['faceRectangle']['top'])
width2 = analysis_face[0]['faceRectangle']['width']
height2 = analysis_face[0]['faceRectangle']['height']
rect2 = patches.Rectangle(rectangle2, width2, height2, linewidth=1,edgecolor='b',facecolor='none')
fig,ax = plt.subplots(1)

# Display the image
ax.imshow(frame)

box1 = [np.array(rectangle), np.array(rectangle) + np.array((height, width))]
box2 = [np.array(rectangle2), np.array(rectangle2) + np.array((height2, width2))]
overlap = (box2[0][0] < box1[1][0] and box2[1][0] > box1[0][0]) and (box2[0][1] < box1[1][1] and box2[1][1] > box1[0][1])

image_caption = 'Overlap: ' + str(overlap) + '  ' 'Identical: ' + str(faces['isIdentical']).capitalize()   
# Add the patch to the Axes
ax.add_patch(rect)
ax.add_patch(rect2)
ax.axis("off")
_ = plt.title(image_caption, size="x-large", y=-0.1)

# When everything done, release the capture
cap.release()
#cv2.destroyAllWindows()
