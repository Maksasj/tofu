from openai import OpenAI
import utils

class Agent:
    def __init__(self, model):
        self.client = OpenAI()
        self.history = []
        self.model = model

    def load_system_prompt(self, filePath):
        self.history.append(
            { "role": "system", "content": utils.read_file_content(filePath)},
        )

    def get_next_command(self):
        completion = self.client.chat.completions.create(
            model = self.model,
            messages = self.history
        )

        return completion.choices[0].message.content.strip()


