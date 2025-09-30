import subprocess
import json

class OllamaWrapper:
    def __init__(self):
        self.models = ['phi', 'mistral', 'llama2', 'tinyllama']
    
    def query_model(self, prompt, model='phi'):
        """Use Ollama CLI instead of API"""
        try:
            # Use subprocess to call ollama directly
            result = subprocess.run(
                ['ollama', 'run', model, prompt],
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.stdout
        except subprocess.TimeoutExpired:
            return "Timeout - model not responding"
        except Exception as e:
            return f"Error: {str(e)}"
    
    def test_all_models(self):
        test_prompt = "Analyze this Middle English: Whan that Aprille"
        for model in self.models:
            print(f"Testing {model}...")
            response = self.query_model(test_prompt, model)
            print(f"  Response: {response[:100]}...")
            print()

# Test
wrapper = OllamaWrapper()
# Just test one model for now
response = wrapper.query_model("test", "phi")
print("Phi response:", response)
