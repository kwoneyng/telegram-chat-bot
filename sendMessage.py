import requests
import pprint
from decouple import config  # decouple 에서부터 config 호출

base_url = 'https://api.telegram.org'
token = config('API_TOKEN')
chat_id = config('CHAT_ID')
text = '디커플 테스트'

api_url = f'{base_url}/bot{token}/sendMessage?chat_id={chat_id}&text={text}'

response = requests.get(api_url)
pprint.pprint(response.json())

#pip install python-decouple