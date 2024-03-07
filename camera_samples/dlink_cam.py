#!/usr/bin/env python
import cv2
import requests
import numpy as np
import sys
import argparse

class Camera():

    def __init__(self, params, show):

        try:
            # Set up the URL of the MJPEG stream
            mjpeg_url = f"http://{params['url']}/{params['stream']}"

            # Set up the username and password for authentication
            username = params['name']
            password = params['password']

            # Make a GET request to the MJPEG stream with HTTP digest authentication
            self.stream = requests.get(mjpeg_url, auth=(username, password), stream=True)

            # Check if the request was successful (HTTP status code 200)
            if self.stream.status_code == 200:
                print("Ready for action!")
            else:
                print("Failed to retrieve MJPEG stream. HTTP status code:", self.stream.status_code)
        except Exception as e:
            print(e)
            sys.exit()

        print('Started connection on: ' + params['url'])

    def show(self):
        bytes = b''

        # Read the MJPEG stream
        for chunk in self.stream.iter_content(chunk_size=1024):
            bytes += chunk
            a = bytes.find(b'\xff\xd8')
            b = bytes.find(b'\xff\xd9')
            if a != -1 and b != -1:
                jpg = bytes[a:b + 2]
                bytes = bytes[b + 2:]
                i = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)

                cv2.imshow('Camera stream', i)
                if cv2.waitKey(1) == 27:
                    exit(0)

if __name__ == '__main__':
    params = {
        "url": "192.168.1.26",
        'name': "admin",
        'password': "E2Wj6i2rA29s",
        "stream": "video1.mjpg",
        'fps': 30
    }
    cam = Camera(params, True)
    cam.show()