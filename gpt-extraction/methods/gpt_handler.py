import base64

from openai import OpenAI


class GPTHandler:
    def __init__(self, openai_key: str, prompt: str):
        self.gpt_client = OpenAI(api_key=openai_key)
        self.prompt = prompt

    # @staticmethod
    # def encode_file(file_bytes):
    #     """Encode the file content to base64."""
    #     return base64.b64encode(file_bytes).decode("utf-8")

    def file_object(self, file_bytes: str):
        file = self.gpt_client.files.create(file=file_bytes, purpose="assistants")
        return file

    def create_assistant(self, file: str, prompt: str, carrier: str):
        assistant = self.gpt_client.beta.assistants.create(
            name=f"Extraction Assistant: {carrier}",
            description=prompt,
            model="gpt-4-1106-preview",
            tools=[{"type": "retrieval"}],
            file_ids=[file.id],
        )
        return assistant

    # def create_thread(self, file):
    #     thread = self.gpt_client.beta.threads.create(
    #         messages=[
    #             {
    #                 "role": "user",
    #                 "content": "Create 3 data visualizations based on the trends in this file.",
    #                 "file_ids": [file.id],
    #             }
    #         ]
    #     )
