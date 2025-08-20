import requests
import json

# The URL of your FastAPI endpoint
# Make sure your server is running (uvicorn main:app --reload)
url = "http://127.0.0.1:8000/ask"

# The query text to send to the API
query_text = "Tell me about the pistol that Ellie uses."

# The JSON payload for the request
payload = {
    "text": query_text
}

# The headers to specify the content type
headers = {
    "Content-Type": "application/json"
}

try:
    # Send the POST request to the API
    print("Sending request to the API...")
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    
    # Check for a successful response (status code 200)
    response.raise_for_status()
    
    # Parse the JSON response
    response_data = response.json()
    
    # Print the response in a readable format
    print("\nAPI Response:")
    print(json.dumps(response_data, indent=4))

except requests.exceptions.RequestException as e:
    print(f"\nAn error occurred: {e}")
except json.JSONDecodeError:
    print("\nError decoding JSON response. The server may have returned a non-JSON response.")
    print("Response content:", response.text)