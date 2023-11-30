import json

import requests


def test_local_endpoint():
    url = "http://localhost:8080"  # Default port for Functions Framework
    headers = {"Content-Type": "application/json"}

    # Sample data that mimics a real request payload
    data = {
        "bucket_name": "audit-bills",
        "file_name": "blueshield_of_california/SUGARED_+_BRONZED_2023_11_30_14_14_03",
        "carrier": "blueshield_of_california",
        "environment": "development",
    }

    response = requests.post(url, data=json.dumps(data), headers=headers)

    print(f"Status code: {response.status_code}")
    print("Response body:")
    print(response.text)


if __name__ == "__main__":
    test_local_endpoint()
