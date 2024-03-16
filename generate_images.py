import json
import time
import requests
import io, base64
from PIL import Image


API_KEY = "EE95D1E89944A30CA8C65182927E4178"
SECRET_KEY = "2A40FC32DBD4FF1588991E45DA26D60B"


class Text2ImageAPI:

    def __init__(self, url, api_key, secret_key):
        self.URL = url
        self.AUTH_HEADERS = {
            'X-Key': f'Key {api_key}',
            'X-Secret': f'Secret {secret_key}',
        }

    def get_model(self):
        response = requests.get(self.URL + 'key/api/v1/models', headers=self.AUTH_HEADERS)
        data = response.json()
        return data[0]['id']

    def generate(self, prompt, model, images=1, width=1024, height=1024):
        params = {
            "type": "GENERATE",
            "numImages": images,
            "width": width,
            "height": height,
            "generateParams": {
                "query": f"{prompt}"
            }
        }

        data = {
            'model_id': (None, model),
            'params': (None, json.dumps(params), 'application/json')
        }
        response = requests.post(self.URL + 'key/api/v1/text2image/run', headers=self.AUTH_HEADERS, files=data)
        data = response.json()
        return data['uuid']

    def check_generation(self, request_id, attempts=10, delay=10):
        while attempts > 0:
            response = requests.get(self.URL + 'key/api/v1/text2image/status/' + request_id, headers=self.AUTH_HEADERS)
            data = response.json()
            if data['status'] == 'DONE':
                return data['images']

            attempts -= 1
            time.sleep(delay)


def get_images(num_images, description, num):
    cnt = 0
    while cnt < num_images:
        api = Text2ImageAPI('https://api-key.fusionbrain.ai/', API_KEY, SECRET_KEY)
        model_id = api.get_model() # создает модели
        uuid = api.generate(description, model_id) # генерирует модель и изображение
        images = api.check_generation(uuid) # проверяет правильность изображения
        img = Image.open(io.BytesIO(base64.decodebytes(bytes(str(images), "utf-8")))) # перевод из строки в фотографию
        img.save(f'/Users/krllggnv/Desktop/images_for_hse_project/my-image{num}.jpeg') # сохранение изображения на устройство
        print(f"Сгенерировано {cnt + 1} из {num_images}")
        cnt += 1
