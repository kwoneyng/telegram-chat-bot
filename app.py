from flask import Flask, escape, request
from decouple import config
import pprint
import requests

app = Flask(__name__)


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

        if text == '점심메뉴' :
            text = '짜장면이나 먹어'

        print('chat_id : ',chat_id)
        print('text : ',text)

    base_url = 'https://api.telegram.org'
    token = config('API_TOKEN')

    api_url = f'{base_url}/bot{token}/sendMessage?chat_id={chat_id}&text={text}'

    response = requests.get(api_url)
    



    return '', 200 # ,뒤의 값 status code



if __name__ == '__main__':
    app.run(debug=True)