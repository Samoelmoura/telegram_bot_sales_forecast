import os
from flask import Flask, request, Response
import pandas as pd
import numpy as np
import requests
from datetime import date
import json

today = str(date.today())
data = {"datetime":today}
data = json.dumps(data)

TOKEN = '6256143671:AAEO718EUVu0qU2IGwtlCeHWqf92QH_B770'
# https://api.telegram.org/bot6256143671:AAEO718EUVu0qU2IGwtlCeHWqf92QH_B770/setWebhook?url=https://sales-forecast-telegram-samoel.herokuapp.com/

def get_data(data):
    url = 'https://sales-forecast-predict-samoel.herokuapp.com/predict'
    headers = {'Content-type':'application/json'}
    data = data
    r = requests.post(url=url, headers=headers, data=data)
    df = pd.DataFrame(r.json())
    return df


def send_message(chat_id, text):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}'
    r = requests.post(url, json={'text':text})
    print(f'Status code = {r.status_code}')
    return None

# instantiate api
app = Flask(__name__)
@app.route('/', methods=['POST'])

def index():
    r = request.get_json()
    if r:
        chat_id = r['message']['chat']['id']
        message = r['message']['text']
        message = str(message).lower()
        message = message.replace('/', '')
        if message == 'abra':
            df = get_data(data)
            next_day_predict = round(df['predict'][0])
            next_week_predict = round(np.sum(df['predict']), 2)
            message = f'CADABRA!!!\nA venda do próximo dia será de: ${next_day_predict}, e a venda da próxima semana será de: ${next_week_predict}'
            send_message(chat_id, message)
            return Response('Ok', status=200)
        else:
            send_message(chat_id, 'Sem permição.')
            return Response('Ok', status=200)
    else:
        pass


if __name__ == '__main__':
    port = os.environ.get('PORT', 5000)
    # port = 5000
    app.run('0.0.0.0', port=port)


