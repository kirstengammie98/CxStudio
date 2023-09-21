import requests
import json

def upload_file(file_name, file_data, generated_url_endpoint):
    generated_url_response = requests.get(generated_url_endpoint, params={'file_name': file_name})
    if generated_url_response.status_code != 200:
        print("Error generating pre-signed URL")
        return

    pre_signed_url = generated_url_response.json().get('upload_url')

    upload_response = requests.put(pre_signed_url, data=file_data)
    if upload_response.status_code == 200:
        print("File uploaded successfully")
    else:
        print("Error uploading file")

if __name__ == "__main__":
    file_name = "example.txt"  
    file_data = b"Hello, World!" 
    generated_url_endpoint = "https://dgj7x94yt4.execute-api.us-east-1.amazonaws.com/prod/generate-url"

    upload_file(file_name, file_data, generated_url_endpoint)
