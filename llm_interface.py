import ollama

class LLMInterface:
    def __init__(self):
        self.config = {
            'model': 'tinyllama',
            'options': {
                'num_thread': 2,
                'num_predict': 32,  # Strict limit
                'temperature': 0.4
            }
        }
    
    def query(self, prompt):
        try:
            response = ollama.chat(
                messages=[{'role': 'user', 'content': f"{prompt} Answer briefly"}],
                **self.config
            )
            return response['message']['content'].strip()
        except:
            return "Let me check that again"