import requests
endpoint = 'ledger/'
url = 'http://localhost:8000/api/'+endpoint
def post_ledger(url, date, from_, to_, amount_, notes_):
    headers = {"content-type": "application/json"}
    data = '''{
        "date": "{date}",
        "from_account": "{from_}",
        "to_account": "{to_}",
        "amount": "{amount_}",
        "notes": "{notes_}"
    }'''
    print(data)
    response = requests.post(url, data=data, headers=headers)
    print(response)

def get(url):
    response = requests.get(url)
    print(response.json())

post_ledger(url, '2020-06-20', 'savings', 'medical', '75.0', 'testing')
