import subprocess
import speech_recognition as sr

class SpeechIO:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.mic = sr.Microphone()
        
        # Direct headphone output config
        self.tts_cmd = 'piper --model en_US-ryan-medium.onnx | aplay -D hw:0,0'

    def speak(self, text):
        subprocess.run(f'echo "{text}" | {self.tts_cmd}', shell=True)

    def listen(self, timeout=2):
        with self.mic as source:
            try:
                audio = self.recognizer.listen(source, timeout=timeout)
                return self.recognizer.recognize_whisper(audio, model="tiny.en")
            except:
                return None

    def shutdown(self):
        self.speak("System shutting down")
