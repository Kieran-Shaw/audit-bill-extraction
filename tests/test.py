import json

import requests

TEST_DATA = ""


def test_local_endpoint():
    url = "http://localhost:8080"  # adjust the port if needed
    headers = {"Content-Type": "application/json"}

    with open(TEST_DATA) as f:
        data = json.load(f)

    response = requests.post(url, data=json.dumps(data), headers=headers)

    print(f"Status code: {response.status_code}")
    print("Response body:")
    print(response.text)


if __name__ == "__main__":
    test_local_endpoint()
