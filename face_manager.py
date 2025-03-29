import face_recognition
import cv2
import pickle

class FaceManager:
    def __init__(self):
        self.known_faces = self._load_db()
    
    def _load_db(self):
        try:
            with open("faces.db", "rb") as f:
                return pickle.load(f)
        except:
            return {}

    def save_db(self):
        with open("faces.db", "wb") as f:
            pickle.dump(self.known_faces, f)

    def process_face(self, face_img):
        # Pi4-optimized processing
        small_face = cv2.resize(face_img, (160, 160))
        encoding = face_recognition.face_encodings(small_face)
        return encoding[0] if encoding else None

    def recognize(self, face_img):
        unknown = self.process_face(face_img)
        if unknown is None: return "Unknown"
        
        for name, known in self.known_faces.items():
            if face_recognition.compare_faces([known], unknown, tolerance=0.55)[0]:
                return name
        return "Unknown"

    def register_face(self, name, face_img):
        if encoding := self.process_face(face_img):
            self.known_faces[name] = encoding
            self.save_db()