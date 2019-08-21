import cognitive_face as CF
import requests
from io import BytesIO
from PIL import Image, ImageDraw

KEY = 'fae20d3fa4dc49eb84a0fe208c900f0d'  # Replace with a valid subscription key (keeping the quotes in place).
CF.Key.set(KEY)

BASE_URL = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0/'  # Replace with your regional Base URL
CF.BaseUrl.set(BASE_URL)

# You can use this example JPG or replace the URL below with your own URL to a JPEG image.
img_url = r'pictures_siem\IMG-20190502-WA0000.jpeg'

face = CF.face.detect(img_url)

faces = CF.face.verify(face[0]['faceId'], person_group_id='test', person_id=siem['personId'])
print(faces)

def getRectangle(faceDictionary):
    rect = faceDictionary['faceRectangle']
    left = rect['left']
    top = rect['top']
    bottom = left + rect['height']
    right = top + rect['width']
    return ((left, top), (bottom, right))

img = Image.open(img_url)
draw = ImageDraw.Draw(img)
for face in face:
    draw.rectangle(getRectangle(face), outline='red')
img.show()

