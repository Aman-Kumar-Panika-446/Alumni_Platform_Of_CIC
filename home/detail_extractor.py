import cv2
import re


def read_qr_from_image(image_path):
    img = cv2.imread(image_path)

    detector = cv2.QRCodeDetector()

    data, bbox, _ = detector.detectAndDecode(img)

    return data if data else None


def split_qr_data(qr_text):
    
    enrollment_no = qr_text[-16:]

    remaining = qr_text[:-16]

    roll_no = re.sub('[^0-9]','',remaining)

    name = re.sub('[^A-Z]','',remaining)

    formatted_name = name  

    return formatted_name, roll_no, enrollment_no
