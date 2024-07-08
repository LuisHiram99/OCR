import pytesseract
import cv2
from PIL import ImageGrab, ImageTk, Image
import numpy as np
from cnocr import CnOcr


class capture_ocr():
    def capture_and_ocr(img_cv):
        # Configure Tesseract path
        pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

        # Perform OCR on the image
        img2char = pytesseract.image_to_string(img_cv)
        print("Captured OCR Text:", img2char)

        # Get bounding boxes for each character (if needed)
        imgbox = pytesseract.image_to_boxes(img_cv)
        imgH, imgW, _ = img_cv.shape

        for boxes in imgbox.splitlines():
            boxes = boxes.split(" ")
            x1, y1, x2, y2 = int(boxes[1]), int(boxes[2]), int(boxes[3]), int(boxes[4])
            cv2.rectangle(img_cv, (x1, imgH - y1), (x2, imgH - y2), (0, 0, 255), 3)

        # Convert BGR to RGB for displaying purposes if needed
        img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img_rgb)
        img_pil.show()  # Show the image with rectangles for verification
        
        return img2char
    
    def cnOCR(img_cv):
            #Perform OCR using CnOcr
            ocr = CnOcr(det_model_name='en_PP-OCRv3_det', rec_model_name='en_PP-OCRv3')
            out = ocr.ocr(img_cv)

            quantity = None
            supplier_pn_value = None

            # Extract relevant information from OCR output
            for index, item in enumerate(out):
                if item['text'] == 'QUANTITY' or item['text'] == 'QTY' and index + 2 < len(out):
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
            
   
    
