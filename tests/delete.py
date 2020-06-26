#!/usr/bin/env python3
import requests
url = 'http://localhost:8000/api/liability/'
response = requests.get(url)
id = ''
for item in list(response.json()):
    print(item)
    if item['notes'] == 'Condo':
        id = str(item['id'])
print(url+id)
response_del = requests.delete(url+id)
print(response_del)
