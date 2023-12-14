import requests


class SensibleExtractor:
    def __init__(self, data, api_key):
        self.data = data
        self.config = data["configuration"]
        self.bill_submission_id = data["id"]
        self.api_key = api_key

    def post_extraction(self, document_url, webhook_url, webhook_payload):
        # Endpoint for Sensible's extract_from_url
        endpoint = f"https://api.sensible.so/v0/extract_from_url/{self.config['document_type']}/{self.config['config_name']}"

        # Prepare headers and payload
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        payload = {
            "document_url": document_url,
            "content_type": "application/pdf",
            "webhook": {"url": webhook_url, "payload": self.data},
        }
        # Send POST request to Sensible
        response = requests.post(endpoint, headers=headers, json=payload)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to initiate extraction: {response.json()}: {self.data}")
            return None
