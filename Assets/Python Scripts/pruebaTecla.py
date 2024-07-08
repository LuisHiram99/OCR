import cv2
import numpy as np
import keyboard
from PIL import ImageGrab
from cnocr import CnOcr  # Assuming capture_ocr.cnOCR is defined in CnOcr module
import UdpComms as U  # Assuming UdpComms is defined in module U

np.seterr(all='ignore')

# Define the area to capture
x, y, width, height = 525, 250, 800, 700

# Create UDP socket to use for sending (and receiving)
sock = U.UdpComms(udpIP="127.0.0.1", portTX=8000, portRX=8001, enableRX=True, suppressWarnings=True)

# Initialize variables
first_capture = True
img1 = None
img_cv1 = None

def cnOCR(img_cv):
    # Perform OCR using CnOcr
    ocr = CnOcr(det_model_name='en_PP-OCRv3_det', rec_model_name='en_PP-OCRv3')
    out = ocr.ocr(img_cv)

    quantity = None
    supplier_pn_value = None

    # Extract relevant information from OCR output
    for index, item in enumerate(out):
        if item['text'] == 'QUANTITY' and index + 2 < len(out):
            quantity = out[index + 2]['text']
        if item['text'] == 'SUPPLIER PN':
            if index + 1 < len(out) and len(out[index + 1]['text']) > 5:
                supplier_pn_value = out[index + 1]['text']
            elif index + 2 < len(out):
                supplier_pn_value = out[index + 2]['text']

    print("-------------------------------------")
    print("quantity:", quantity)
    print("supplier-pn:", supplier_pn_value)
    print("-------------------------------------")

    return quantity, supplier_pn_value

def take_screenshot():
    global first_capture, img1, img_cv1

    if first_capture:
        # Capture the first screen area
        img1 = ImageGrab.grab(bbox=(x, y, x + width, y + height))
        img_np1 = np.array(img1)
        img_cv1 = cv2.cvtColor(img_np1, cv2.COLOR_RGB2BGR)
        
        # Display the first screenshot
        cv2.imshow("First Screenshot", img_cv1)
        cv2.waitKey(0)  # Wait for a key press to close the window
        
        first_capture = False
        print("First image captured.")
    else:
        # Capture the second screen area
        img2 = ImageGrab.grab(bbox=(x, y, x + width, y + height))
        img_np2 = np.array(img2)
        img_cv2 = cv2.cvtColor(img_np2, cv2.COLOR_RGB2BGR)
        
        # Display the second screenshot
        cv2.imshow("Second Screenshot", img_cv2)
        cv2.waitKey(0)  # Wait for a key press to close the window
        
        # Perform OCR on both images
        text1 = cnOCR(img_cv1)
        text2 = cnOCR(img_cv2)

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

# Register the screenshot function to be called on key press
keyboard.add_hotkey('space', take_screenshot)

# Keep the program running to listen for key presses
print("Press 'space' to take a screenshot and perform OCR. Press 'esc' to exit.")
keyboard.wait('esc')

# Close all OpenCV windows when done
cv2.destroyAllWindows()