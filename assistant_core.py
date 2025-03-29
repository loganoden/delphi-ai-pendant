import cv2
import time
from network_client import VisionClient
from face_manager import FaceManager
from llm_interface import LLMInterface
from speech_io import SpeechIO

class AssistantCore:
    def __init__(self):
        self.vision = VisionClient("192.168.1.5")
        self.faces = FaceManager()
        self.llm = LLMInterface()
        self.speech = SpeechIO()
        self.cap = cv2.VideoCapture(0)
        
        # Ethernet-optimized camera settings
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        self.cap.set(cv2.CAP_PROP_FPS, 15)

    def run(self):
        last_announce = {}
        try:
            while True:
                ret, frame = self.cap.read()
                if not ret: break

                # Get detections from Pi5
                faces = self.yolo.get_faces(frame)
                
                for (x1, y1, x2, y2) in faces:
                    face_img = frame[y1:y2, x1:x2]
                    name = self.faces.recognize(face_img)
                    
                    if name == "Unknown":
                        self.handle_new_face(face_img)
                        continue
                        
                    self.announce_presence(name, last_announce)

                if cv2.waitKey(1) == ord('q'):
                    break

        finally:
            self.cap.release()
            self.speech.shutdown()

    def handle_new_face(self, face_img):
        self.speech.speak("New person detected. Please say their name.")
        if (name := self.speech.listen()):
            self.faces.register_face(name, face_img)
            self.speech.speak(f"{name} has been registered")

    def announce_presence(self, name, last_announce):
        if time.time() - last_announce.get(name, 0) > 30:
            self.speech.speak(f"{name} is present")
            context = self.llm.query(f"Brief description of {name}")
            self.speech.speak(context)
            last_announce[name] = time.time()