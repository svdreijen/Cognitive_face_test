# Import libraries
import numpy as np
import cv2
import matplotlib.patches as patches
import requests
import matplotlib.pyplot as plt
import json

# Define functions to post request to face and vision API's
def detect_face(pic):
    headers     = {'Ocp-Apim-Subscription-Key' : subscription_key_face,
                    'Content-Type': 'application/octet-stream'}

    params      = {'returnFaceLandmarks' : 'True'}

    response = requests.post(
        face_api_url + "detect", headers=headers, params=params, data=pic)

    response.raise_for_status()

    analysis_face = response.json()
    return analysis_face
def verify_face(faceId, personId, personGroupId):
    headers     = {'Ocp-Apim-Subscription-Key' : subscription_key_face,
                    'Content-Type' : 'application/json'}

    data        = {'faceId' : faceId,
                    'personId' : personId,
                    'personGroupId': personGroupId}

    data = json.dumps(data)

    response = requests.post(
        face_api_url + "verify", headers=headers, data=data)

    response.raise_for_status()

    analysis_verify = response.json()
    return analysis_verify
def object_analysis(pic):
    headers    = {'Ocp-Apim-Subscription-Key': subscription_key_vision,
                'Content-Type': 'application/octet-stream'}

    params     = {'visualFeatures': 'Objects'}

    response = requests.post(
        vision_base_url + 'analyze', headers=headers, params=params, data=pic)

    response.raise_for_status()

    analysis = response.json()
    return analysis

# Define the keys and api urls for face api
subscription_key_face = '6fa0509cc7a64886a6775e56ec98d763'
face_api_url = 'https://westeurope.api.cognitive.microsoft.com/face/v1.0/'

# Define the keys and api urls for vision api
subscription_key_vision = "4303a199f4c749bf911015d6dd999ae3"
vision_base_url = "https://westeurope.api.cognitive.microsoft.com/vision/v2.0/"


# Capture webcam stream and read out frame
cap = cv2.VideoCapture(0)
ret, frame = cap.read()

# Convert the frame numpy array to .jpg binary string
frame_str = cv2.imencode('.jpg', frame)[1].tostring()

# Detect the face in the picture
analysis_face = detect_face(frame_str)

# Verify if the detected face matches person database
if analysis_face:
    analysis_verify = verify_face(analysis_face[0]['faceId'], siem['personId'], 'test')

# Detect object in the picture
analysis = object_analysis(frame_str)

# Create a Rectangle
# For the object
if analysis['objects']:
    rectangle = (analysis['objects'][0]['rectangle']['x'], analysis['objects'][0]['rectangle']['y'])
    width = analysis['objects'][0]['rectangle']['w']
    height = analysis['objects'][0]['rectangle']['h']
    rect = patches.Rectangle(rectangle, width, height, linewidth=1,edgecolor='r',facecolor='none')
    box1 = [np.array(rectangle), np.array(rectangle) + np.array((height, width))]

# For the face
if analysis_face:
    rectangle2 = (analysis_face[0]['faceRectangle']['left'], analysis_face[0]['faceRectangle']['top'])
    width2 = analysis_face[0]['faceRectangle']['width']
    height2 = analysis_face[0]['faceRectangle']['height']
    rect2 = patches.Rectangle(rectangle2, width2, height2, linewidth=1,edgecolor='b',facecolor='none')
    box2 = [np.array(rectangle2), np.array(rectangle2) + np.array((height2, width2))]

# Display the image
fig,ax = plt.subplots(1)
ax.imshow(frame)

# Draw the boxes around face and object
if analysis['objects']:
    ax.add_patch(rect)
if analysis_face:
    ax.add_patch(rect2)
ax.axis("off")
_ = plt.title(image_caption, size="x-large", y=-0.1)

# Determine whether face and object overlap
overlap = (box2[0][0] < box1[1][0] and box2[1][0] > box1[0][0]) and (box2[0][1] < box1[1][1] and box2[1][1] > box1[0][1])
image_caption = 'Overlap: ' + str(overlap) + '  ' 'Identical: ' + str(faces['isIdentical']).capitalize()   

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
