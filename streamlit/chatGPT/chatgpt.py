import json
import requests


def call_chatgpt_api(quest):
    auth_token = "INSIRA-SUA-CHAVE-AQUI"
    header = {
        "Authorization": "Bearer " + auth_token
    }
    data = {
        "model": "text-davinci-003",
        "prompt": quest,
        "temperature": 1,
        "max_tokens": 500
    }

    # API
    url = "https://api.openai.com/v1/completions"
    resp = requests.post(url, json=data, headers=header)
    return resp.text


def process_response(elements):
    try:
        return json.loads(elements)['choices'][0]['text'].strip() 
    except KeyError:
        return json.loads(elements)['error']['message'].strip()
    except Exception:
        return "Unknown error."


if __name__ == '__main__':
    question = input("Insira sua pergunta: ")
    print(process_response(call_chatgpt_api(question)))