import base64
import json
import os

import requests
from dotenv import load_dotenv

load_dotenv()
SENSIBLE_KEY = os.getenv("SENSIBLE_KEY")

DOCUMENT_TYPE = "bill_metdata"
CONFIG_NAME = "kaiser"
FILE_PATH = "/Users/kieranshaw/Downloads/Kaiser Group Premium Bill.pdf"
SAVE_PATH = (
    "/Users/kieranshaw/audit-bill-extraction/responses/sensible_kaiser_response.json"
)

with open(FILE_PATH, "rb") as file:
    file_bytes = file.read()
    encoded_document = base64.b64encode(file_bytes).decode("utf-8")


url = f"https://api.sensible.so/v0/extract/{DOCUMENT_TYPE}/{CONFIG_NAME}?environment=development"

payload = {"document": encoded_document}

headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "authorization": f"Bearer {SENSIBLE_KEY}",
    "document_name": FILE_PATH,
}

response = requests.post(url, json=payload, headers=headers)

if response.status_code == 200:
    # Parse response
    data = response.json()

    # Write to a file
    with open(SAVE_PATH, "w") as json_file:
        json.dump(data, json_file, indent=4)
