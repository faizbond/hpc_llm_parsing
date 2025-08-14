import requests
import json

# The endpoint for oobabooga's OpenAI-compatible API
api_url = "http://127.0.0.1:5000/v1/chat/completions"

# Request payload
payload = {
    "model": "gpt-3.5-turbo",  # model name is ignored in some setups but required by API format
    "messages": [
        {"role": "user", "content": "What is the synthesis condition of MOF-5?"}
    ],
    "temperature": 0.7
}

# Send request
response = requests.post(api_url, json=payload)

# Parse and print the response text
if response.status_code == 200:
    result = response.json()
    print(result["choices"][0]["message"]["content"])
else:
    print(f"Error {response.status_code}: {response.text}")

