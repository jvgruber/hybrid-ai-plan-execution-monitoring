import requests
API_URL = "https://api-inference.huggingface.co/models/meta-llama/Llama-2-70b-chat-hf"
API_TOKEN = "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"
headers = {"Authorization": f"Bearer {API_TOKEN}"}
def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    # try:
    #     response.raise_for_status()  # Check if the request was successful
    return response.json()  # Parse JSON response
    # except requests.exceptions.HTTPError as http_err:
    #     print(f"HTTP error occurred: {http_err}")  # Print HTTP error
    # except requests.exceptions.RequestException as req_err:
    #     print(f"Request error occurred: {req_err}")  # Print request error
    # except ValueError:
    #     print(f"Invalid JSON received: {response.text}")  # Print response content if JSON parsing fails
    # return None
data = query("Can you please let us know more details about your ")
print(data)