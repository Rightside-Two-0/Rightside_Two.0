import requests, json

url = 'http://localhost:8000/api/opportunity/'
headers = {"content-type": "application/json"}
data_dict = {
    'heading': 'Duplex, Condemed',
    'description': 'Needs work - Rehab project!',
    'url': 'https://www.crexi.com/properties/352618/pennsylvania-530-theodore-st',
    'cost': '39000.0',
    'down': '11,700.00',
    'mortgage': '27,300.00',
    'cash_flow': '752.54',
    'coc': '0.77', 
    'irr': '15.00',
    'ask': '39000',
    'sqft': '1600',
    'units': '2',
    'ave_rent': '650',
    'vacancy_rate': '.1',
    'other_income': '0',
    'repairs': '50' ,
    'management': '50',
    'taxes': '50',
    'insurance': '50',
    'wages': '0', 
    'utilities': '50',
    'gen_admin': '50',
    'professional_fees': '50',
    'advertising': '0',
    'cap_x': '50',
    'other': '0'
}   
data = json.dumps(data_dict)
print(data)
response = requests.post(url, data=data, headers=headers)
print(response.status_code)