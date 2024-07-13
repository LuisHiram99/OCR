import cv2
import numpy as np
import keyboard
from PIL import ImageGrab

np.seterr(all='ignore')

# Define the area to capture
x, y, width, height = 150, 150, 1600, 850

# Initialize variables
first_capture = True
img1 = None
img_cv1 = None

def take_screenshot():
    global first_capture, img1, img_cv1

    if first_capture:
        # Capture the screen area
        img1 = ImageGrab.grab(bbox=(x, y, x + width, y + height))
        img_np1 = np.array(img1)
        img_cv1 = cv2.cvtColor(img_np1, cv2.COLOR_RGB2BGR)
        
        # Display the screenshot
        cv2.imshow("Screenshot", img_cv1)
        cv2.waitKey(0)  # Wait for a key press to close the window
        
        first_capture = False
        print("Screenshot captured.")
    else:
        # Capture the screen area again
        img2 = ImageGrab.grab(bbox=(x, y, x + width, y + height))
        img_np2 = np.array(img2)
        img_cv2 = cv2.cvtColor(img_np2, cv2.COLOR_RGB2BGR)
        
        # Display the second screenshot
        cv2.imshow("Screenshot", img_cv2)
        cv2.waitKey(0)  # Wait for a key press to close the window
        
        # Reset for the next capture
        first_capture = True
        img1 = None
        img_cv1 = None

# Register the screenshot function to be called on key press
keyboard.add_hotkey('space', take_screenshot)

# Keep the program running to listen for key presses
print("Press 'space' to take a screenshot. Press 'esc' to exit.")
keyboard.wait('esc')

# Close all OpenCV windows when done
cv2.destroyAllWindows()
