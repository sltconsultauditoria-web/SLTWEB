import requests

def test_auth():
    url = "http://localhost:8000/api/auth/login"
    payload = {
        "email": "admin@empresa.com",
        "password": "admin123"
    }
    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        print("Autenticação bem-sucedida!", response.json())
    else:
        print("Falha na autenticação.", response.status_code, response.text)

if __name__ == "__main__":
    test_auth()