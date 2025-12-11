# crear_usuario.py
import requests

response = requests.post('http://localhost:8000/api/register', json={
    'username': 'sole',
    'email': 'cristianvillalba439@yahoo.com.ar',
    'password': 'sole1550'
})

print(response.json())