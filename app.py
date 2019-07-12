from flask import Flask, escape, request
from decouple import config
import pprint
import requests
app = Flask(__name__)

API_TOKEN = config('API_TOKEN')
NAVER_CLIENT_ID = config('NAVER_CLIENT_ID')
NAVER_CLIENT_SECRET = config('NAVER_CLIENT_SECRET')

API_TOKEN = config('API_TOKEN')

@app.route('/')
def hello():
    name = request.args.get("name", "World")
    return 'Hello, World!'


@app.route('/greeting/<name>')
def greeting(name):
    return f'Hello, {name}'


@app.route(f'/{API_TOKEN}', methods=['POST'])
def telegram():
    from_telegram = request.get_json()
#    pprint.pprint(from_telegram)
    if from_telegram.get('message') is not None:
        chat_id = from_telegram.get('message').get('chat').get('id')
        text = from_telegram.get('message').get('text')

        # 처음 네글자가 '/번역' 일 때        
        if text[0:4] == '/한영 ':
            #요청에 대한 정보가 저장되어있다.
            headers = {
                'X-Naver-Client-Id': NAVER_CLIENT_ID,
                'X-Naver-Client-Secret': NAVER_CLIENT_SECRET,
            }
            data = {
                'source': 'ko',
                'target': 'en',
                'text': text[4:]
            }
            papago_url = 'https://openapi.naver.com/v1/papago/n2mt'
            papago_res = requests.post(papago_url, headers=headers, data=data)
            text = papago_res.json().get('message').get('result').get('translatedText')
            

        if text[0:4] == '/영한 ':
            #요청에 대한 정보가 저장되어있다.
            headers = {
                'X-Naver-Client-Id': NAVER_CLIENT_ID,
                'X-Naver-Client-Secret': NAVER_CLIENT_SECRET,
            }
            data = {
                'source': 'en',
                'target': 'ko',
                'text': text[4:]
            }

            papago_url = 'https://openapi.naver.com/v1/papago/n2mt'
            papago_res = requests.post(papago_url, headers=headers, data=data)
            text = papago_res.json().get('message').get('result').get('translatedText')

    base_url = 'https://api.telegram.org'
    token = config('API_TOKEN')

    api_url = f'{base_url}/bot{token}/sendMessage?chat_id={chat_id}&text={text}'

    response = requests.get(api_url)
    
    return '', 200 # ,뒤의 값 status code



if __name__ == '__main__':
    app.run(debug=True)