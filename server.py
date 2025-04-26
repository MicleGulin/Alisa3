# импортируем библиотеки
from flask import Flask, request, jsonify
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
sessionStorage = {}


@app.route('/post', methods=['POST'])
def main():
    logging.info(f'Request: {request.json!r}')

    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }

    handle_dialog(request.json, response)

    logging.info(f'Response:  {response!r}')

    # Преобразовываем в JSON и возвращаем
    return jsonify(response)


def handle_dialog(req, res):
    user_id = req['session']['user_id']

    if req['session']['new']:
        sessionStorage[user_id] = {
            'suggests': [
                "Не хочу.",
                "Не буду.",
                "Отстань!"
            ],
            'status': 'elefant'
        }
        res['response']['text'] = 'Привет! Купи слона!'
        res['response']['buttons'] = get_suggests(user_id)
        return

    if [i for i in req['request']['nlu']['tokens'] if i in ['ладно', 'куплю', 'покупаю', 'хорошо']]:

        if sessionStorage[user_id]['status'] == 'elefant':
            sessionStorage[user_id]['status'] = 'rabbit'
            res['response']['text'] = 'Слона можно найти на Яндекс.Маркете! А теперь купи кролика'
        elif sessionStorage[user_id]['status'] == 'rabbit':
            sessionStorage[user_id]['status'] = 'elefant'
            res['response']['text'] = 'Кролика можно найти на Яндекс.Маркете! А теперь купи слона'

        return
    if sessionStorage[user_id]['status'] == 'elefant':
        res['response']['text'] = \
            f"Все говорят '{req['request']['original_utterance']}', а ты купи слона!"
    else:
        res['response']['text'] = \
            f"Все говорят '{req['request']['original_utterance']}', а ты купи кролика!"
    res['response']['buttons'] = get_suggests(user_id)


def get_suggests(user_id):
    session = sessionStorage[user_id]

    suggests = [
        {'title': suggest, 'hide': True}
        for suggest in session['suggests'][:2]
    ]

    session['suggests'] = session['suggests'][1:]
    sessionStorage[user_id] = session
    if session['status'] == 'elefant':
        if len(suggests) < 2:
            suggests.append({
                "title": "Ладно",
                "url": "https://market.yandex.ru/search?text=слон",
                "hide": True
            })

    if session['status'] == 'rabbit':
        if len(suggests) < 2:
            suggests.append({
                "title": "Ладно",
                "url": "https://market.yandex.ru/search?text=кролик",
                "hide": True
            })
    return suggests


if __name__ == '__main__':
    app.run()
