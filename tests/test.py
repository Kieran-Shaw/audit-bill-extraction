import json

import requests

JSON_TEST_FILE_PATH = (
    "/Users/kieranshaw/audit-bill-extraction/tests/blue_shield_test.json"
)


def test_local_endpoint(json_file_path):
    url = "http://localhost:8080"  # Default port for Functions Framework
    headers = {"Content-Type": "application/json"}

    # Read data from JSON file
    with open(json_file_path, "r") as file:
        data = json.load(file)

    response = requests.post(url, data=json.dumps(data), headers=headers)

    print(f"Status code: {response.status_code}")
    print("Response body:")
    print(response.text)


if __name__ == "__main__":
    test_local_endpoint(JSON_TEST_FILE_PATH)
