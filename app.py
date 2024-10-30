import os
from dotenv import load_dotenv
import requests

FILE_PATH = 'dane.txt'
GET_URL = 'https://poligon.aidevs.pl/dane.txt'
SEND_URL = 'https://poligon.aidevs.pl/verify'

load_dotenv()


def download_file(url, path):
    response = requests.get(url)
    with open(path, 'wb') as file:
        file.write(response.content)


def read_file(path):
    lines = []
    with open(path, 'r') as file:
        for line in file.readlines():
            lines.append(line.strip())
    return lines


def get_data():
    download_file(GET_URL, FILE_PATH)
    data = read_file(FILE_PATH)
    os.remove(FILE_PATH)
    return data


def send_data(data):
    response = requests.post(SEND_URL, json=data)
    return response.json()


data = get_data()

query = {
    "task": os.getenv('TASK_NAME'),
    "apikey": os.getenv('AI_DEV_API_KEY'),
    "answer": data
}

response = send_data(query)
print(response)
