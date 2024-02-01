import requests
from requests.auth import HTTPBasicAuth

username = 'admin'
password = 'qwe123@A'

def auth_api():
    api_url = 'http://127.0.0.1:5000/api/v1/list_audiences/'

    response = requests.get(api_url, auth=HTTPBasicAuth(username, password))

    if response.status_code == 200:

        response_json = response.json()        
        return response_json

    else:
        # Exibe uma mensagem de erro se a solicitação falhar
        print(f"Erro na solicitação: {response.status_code} - {response.text}")

def remove_aud(audience_id):
    api_url = f'http://127.0.0.1:5000/api/v1/delete/{audience_id}'

    response = requests.get(api_url, auth=HTTPBasicAuth(username, password))

    if response.status_code == 200:

        response_json = response.json()        
        return response_json

    else:
        # Exibe uma mensagem de erro se a solicitação falhar
        print(f"Erro na solicitação: {response.status_code} - {response.text}")