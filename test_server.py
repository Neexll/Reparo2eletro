#!/usr/bin/env python3
import requests
import sys

try:
    response = requests.get('http://127.0.0.1:5000/')
    print(f'Status Code: {response.status_code}')

    if response.status_code == 200:
        print('SUCCESS! Página carregou corretamente!')
        print(f'Content Length: {len(response.text)}')
    else:
        print('ERROR RESPONSE:')
        print(response.text)

except requests.exceptions.ConnectionError:
    print('ERROR: Não foi possível conectar ao servidor. Certifique-se de que ele está rodando.')
except Exception as e:
    print(f'ERROR: {e}')
    sys.exit(1)
