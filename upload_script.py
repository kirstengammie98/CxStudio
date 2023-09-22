import requests

def upload_file(id, file_data, generated_url_endpoint):
    generated_url_response = requests.get(generated_url_endpoint, params={'id': id})
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
    id = "example.txt"  
    file_data = b"Hello, World!" 
    generated_url_endpoint = "https://dgj7x94yt4.execute-api.us-east-1.amazonaws.com/prod/generate-url"

    upload_file(id, file_data, generated_url_endpoint)
