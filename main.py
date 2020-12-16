import streamlit as st
import requests
from PIL import Image, ImageDraw
import json
import io

def face_recognition():				
	st.title('Face Recognition App')

	subscription_key = st.sidebar.text_input('Enter your API key for Azure Face API', type="password")
		
	assert subscription_key

	root_url = 'https://20201215-pecop.cognitiveservices.azure.com/'
	endpoint_url = 'face/v1.0/detect'
	face_api_url = root_url + endpoint_url 

	headers = {
		    'Content-Type': 'application/octet-stream',
		    'Ocp-Apim-Subscription-Key': subscription_key
		}

	params = {
		    'returnFaceId': 'true',
		    'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise',
		}

	uploaded_file = st.file_uploader('Choose an image.', type='jpg')

	if uploaded_file is not None:
		img = Image.open(uploaded_file)

		with io.BytesIO() as output:
		    img.save(output, format='JPEG')
		    binary_img = output.getvalue()

		try:
			res = requests.post(face_api_url, params=params, headers=headers, data=binary_img)
		except Exception as e:
			st.sidebar.warning('Your API key is invalid.')

		results = res.json()

		for result in results:
		    rect = result['faceRectangle']
		    draw = ImageDraw.Draw(img)
		    draw.rectangle([(rect['left'], rect['top']), (rect['left']+rect['width'], rect['top']+rect['height'])], fill=None, outline='gold', width=10)

		st.image(img, caption='Uploaded Image', use_column_width=True)


if __name__ == '__main__':
	face_recognition()