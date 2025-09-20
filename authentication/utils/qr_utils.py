import cv2
import re
from datetime import datetime
def read_qr_from_image(image_path):
    img = cv2.imread(image_path)
    detector = cv2.QRCodeDetector()
    data, bbox, _ = detector.detectAndDecode(img)
    return data if data else None

def split_qr_data(qr_text):
    enrollment_no = qr_text[-16:]
    remaining = qr_text[:-16]
    roll_no = re.sub('[^0-9]', '', remaining)
    formatted_name = re.sub('[^A-Z]', '', remaining)
    
    starting_year = 2000 + (int(enrollment_no[0:2]))
    ending_year = starting_year + 4
    current_year = datetime.now().year

    if( (ending_year < current_year) or (ending_year == current_year and datetime.now().month >6) ):
        role = 'Alumni'
    else:
        role = 'Student'

    return formatted_name, roll_no, enrollment_no, starting_year, ending_year, role
