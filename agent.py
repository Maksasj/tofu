from openai import OpenAI
import utils

class Agent:
    def __init__(self, model):
        self.client = OpenAI()
        self.history = []
        self.model = model

    def load_system_prompt(self, filePath):
        self.history.append({ 
            "role": "system", 
            "content": utils.read_file_content(filePath)
        })

    def load_user_prompt(self, prompt):
        self.history.append({
            "role": "user",
            "content": prompt
        })

    def get_next_command(self):
        completion = self.client.chat.completions.create(
            model = self.model,
            messages = self.history
        )

        self.history.append({
            "role": "assistant",
            "content": completion.choices[0].message.content.strip()
        })

        return completion.choices[0].message.content.strip()

    def save_command_result(self, result):
        self.history.append({
            "role": "user",
            "content": result
        })
