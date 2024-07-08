# Created by Youssef Elashry to allow two-way communication between Python3 and Unity to send and receive strings

# Feel free to use this in your individual or commercial projects BUT make sure to reference me as: Two-way communication between Python 3 and Unity (C#) - Y. T. Elashry
# It would be appreciated if you send me how you have used this in your projects (e.g. Machine Learning) at youssef.elashry@gmail.com

# Use at your own risk
# Use under the Apache License 2.0

# Example of a Python UDP server

import UdpComms as U
import time
import pytesseract
import cv2
from PIL import ImageGrab, ImageTk, Image
import numpy as np
from OCR import capture_ocr

global first_capture, img1, img_cv1

# Define the screen area to capture (x, y, width, height)
x, y, width, height = 525, 250, 800, 700

# Create UDP socket to use for sending (and receiving)
sock = U.UdpComms(udpIP="127.0.0.1", portTX=8000, portRX=8001, enableRX=True, suppressWarnings=True)

first_capture = True
img1 = None

while True:
    data = sock.ReadReceivedData()  # read data

    if data is not None:
        if first_capture:
            # Capture the first screen area
            img1 = ImageGrab.grab(bbox=(x, y, x + width, y + height))
            img_np1 = np.array(img1)
            img_cv1 = cv2.cvtColor(img_np1, cv2.COLOR_RGB2BGR)
            first_capture = False
            print("First image captured.")
            text1 = capture_ocr.cnOCR(img_cv1)
        else:
            # Capture the second screen area
            img2 = ImageGrab.grab(bbox=(x, y, x + width, y + height))
            img_np2 = np.array(img2)
            img_cv2 = cv2.cvtColor(img_np2, cv2.COLOR_RGB2BGR)
            print("Second image captured.")
            text2 = capture_ocr.cnOCR(img_cv2)

            # Compare OCR texts
            if text1 == text2:
                comparison_result = "Both texts are the same"
            else:
                comparison_result = "Texts are not the same"

            print(comparison_result)

            # Reset for the next capture
            first_capture = True
            img1 = None
            img_cv1 = None

            # Send comparison result to Unity
            sock.SendData('OCR Comparison: ' + comparison_result)

    time.sleep(1)