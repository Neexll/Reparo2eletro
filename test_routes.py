#!/usr/bin/env python3
import requests
import traceback

def test_route_detailed(route_name, route_path):
    print(f"\n=== Testando {route_name} ===")
    try:
        response = requests.get(f'http://127.0.0.1:5000{route_path}', timeout=5)
        print(f'Status: {response.status_code}')

        if response.status_code == 200:
            print('SUCCESS!')
            content_length = len(response.text)
            print(f'Content length: {content_length} characters')
            if content_length > 0:
                print(f'First 200 chars: {response.text[:200]}')
        else:
            print('ERROR RESPONSE:')
            print(response.text)

    except requests.exceptions.ConnectionError:
        print('ERROR: Cannot connect to server')
    except Exception as e:
        print(f'ERROR: {e}')
        traceback.print_exc()

if __name__ == '__main__':
    test_route_detailed('INDEX', '/')
    test_route_detailed('DASHBOARD', '/dashboard')
    test_route_detailed('MANAGE_PECAS', '/manage_pecas')
    test_route_detailed('MANAGE_TECNICOS', '/manage_tecnicos')
