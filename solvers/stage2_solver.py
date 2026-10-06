import requests

print('Attempting to log in as Adrian Kessler...')
url = 'http://localhost:3000/rest/user/login'
data = {'email': 'adrian.kessler@uninvited.local', 'password': 'Kessler123!'}

try:
    response = requests.post(url, json=data)
    if response.status_code == 200:
        print('[+] Login Successful!')
        token = response.json().get('data', {}).get('token', response.json().get('authentication', {}).get('token'))
        print(f'[+] JWT Token: {str(token)[:40]}...')
    else:
        print('[-] Login failed.')
except Exception as e:
    print(f'Error: {e}')
