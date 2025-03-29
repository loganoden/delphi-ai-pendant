from speech_io import SpeechIO
import time

def test_speech():
    speech = SpeechIO()
    
    print("Testing text-to-speech...")
    speech.speak("Hello! This is a speech test. Please say something after the beep.")
    
    print("Listening for 5 seconds...")
    start_time = time.time()
    while time.time() - start_time < 5:
        speech.speak(".")  # Short beep
        response = speech.listen(timeout=3)
        if response:
            print(f"Heard: {response}")
            speech.speak(f"You said: {response}")
            return
    
    speech.speak("No input detected")

if __name__ == "__main__":
    test_speech()