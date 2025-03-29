import requests
import cv2
import numpy as np

class VisionClient:
    def __init__(self, server_ip="192.168.1.5"):
        self.detect_url = f"http://{server_ip}:8000/detect"

    def get_faces(self, frame):
        # Compress and send frame to Pi 5
        _, img_encoded = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 70])
        try:
            response = requests.post(
                self.detect_url,
                data=img_encoded.tobytes(),
                headers={'Content-Type': 'image/jpeg'},
                timeout=1.0
            )
            return response.json()
        except:
            return []
        
        #172.30.15.86