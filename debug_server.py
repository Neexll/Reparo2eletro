#!/usr/bin/env python3
import subprocess
import time
import requests
import sys

# Start Flask server with debug
server_process = subprocess.Popen([
    sys.executable, '-c',
    '''
from app import app
app.run(debug=True, use_reloader=False, port=5001)
    '''
], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

# Wait a moment for server to start
time.sleep(3)

try:
    # Try to make a request
    response = requests.get('http://127.0.0.1:5001/', timeout=5)
    print(f'Status Code: {response.status_code}')

    if response.status_code == 500:
        print('ERROR 500 - Internal Server Error')
        # Try to get more details from server output
        output, error = server_process.communicate(timeout=5)
        if error:
            print('SERVER ERROR OUTPUT:')
            print(error)
    else:
        print('SUCCESS!')

except requests.exceptions.RequestException as e:
    print(f'Connection error: {e}')
    server_process.terminate()
except subprocess.TimeoutExpired:
    print('Server process timed out')
    server_process.terminate()
finally:
    server_process.terminate()
