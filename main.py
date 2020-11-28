import requests
from urllib.parse import urljoin
from pprint import pprint
import time
import json
import tqdm

TOKEN_VK = ''
TOKEN_YADISK = ''
API_BASE_URL = 'https://api.vk.com/method/'
V = '5.21'
FOLDER_NAME = 'vk_photo/'
print('Резервное копирование')
token_vk = (input('Введите токен пользователя vk: '))
token_yadisk = input('Введите токен Яндекс.Диска: ')


class VkUser:
  def __init__(self, token=token_vk, version=V):
    self.token = token
    self.version = version

  def photos_get_id(self):
    photos_get_id = urljoin(API_BASE_URL, 'photos.get')
    response = requests.get(photos_get_id, params={
      'access_token': self.token,
      'v': self.version,
      'album_id': 'profile',
      'rev': 1,  
      'extended': 1,  
      'photo_sizes': 1,
      'count': 1000, 
      })
    return response.json()['response']['items']



class YaUploader:
  def __init__(self, token):
    self.token = token

  def create_folder(self, folder_name):
    HEADERS = {'Authorization': f'OAuth {self.token}'}
    requests.put(
      'https://cloud-api.yandex.net/v1/disk/resources',
      params={'path': folder_name},
      headers=HEADERS
  )
    return folder_name

  def upload(self, file_name, file_url):
    HEADERS = {'Authorization': f'OAuth {self.token}'}
    FILE = file_name
    URL = file_url

    requests.post(
      'https://cloud-api.yandex.net/v1/disk/resources/upload',
      params={'path': FILE, 'url': URL},
      headers=HEADERS,
  )
    return file_url, file_name

  def publish(self):
    folder = uploader.create_folder(FOLDER_NAME)
    photos = user.photos_get_id()
    json_list = []
    for photo_info in tqdm.tqdm(photos):
      photo_url = photo_info['sizes'][-1]['src']
      photo_size = photo_info['sizes'][-1]['type']
      likes = photo_info['likes']['count']
      photo_data = photo_info['date']
      upload_time = time.ctime(photo_data).replace(':', ';')
      photo_name = f'{str(likes)}, {upload_time}'

      info = {'file_name': photo_name, 'size': photo_size}
      json_list.append(info)
      uploader.upload((folder + photo_name + 'jpg'), photo_url)

    with open('info.json', 'w', encoding='utf-8') as f:
      json.dump(json_list, f, indent=1)
    with open('info.json', 'r') as f:
      data = json.load(f)
      print('Информация по файлу:')
      pprint(data)

    print('Измененный Яндекс.диск, куда добавились фотографии:')
    print('https://disk.yandex.ru/client/disk/' + folder)

if __name__ == "__main__":
  user = VkUser()
  uploader = YaUploader(token_yadisk)
  uploader.publish()
