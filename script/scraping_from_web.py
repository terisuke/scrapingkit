from dotenv import load_dotenv
import os
import hashlib
import math
import requests
import urllib
import json
from PIL import Imag

load_dotenv()


def make_dir(path):
    if not os.path.isdir(path):
        os.mkdir(path)


def make_correspondence_table(correspondence_table, original_url, hashed_url):
    correspondence_table[original_url] = hashed_url


def make_img_path(save_dir_path, url, correspondence_table):
    save_img_path = os.path.join(save_dir_path, 'imgs')
    make_dir(save_img_path)

    file_extension = os.path.splitext(url)[-1]
    if file_extension.lower() in ('.jpg', '.jpeg', '.gif', '.png', '.bmp'):
        encoded_url = url.encode('utf-8')
        hashed_url = hashlib.sha3_256(encoded_url).hexdigest()
        full_path = os.path.join(save_img_path, hashed_url + file_extension.lower())

        make_correspondence_table(correspondence_table, url, hashed_url)
        return full_path
    else:
        raise ValueError('Not applicable file extension')


def download_image(url):
    response = requests.get(url, allow_redirects=True)
    if response.status_code != 200:
        raise Exception("HTTP status: " + response.status_code)

    content_type = response.headers["content-type"]
    if 'image' not in content_type:
        raise Exception("Content-Type: " + content_type)

    return response.content


def save_image(filename, image):
    with open(filename, "wb") as fout:
        fout.write(image)


if __name__ == "__main__":
    save_dir_path = '/Users/teradakousuke/Library/Mobile Documents/com~apple~CloudDocs/Scriping tool/BrailleBlock'
    make_dir(save_dir_path)

    num_imgs_required = 1000
    num_imgs_per_transaction = 150
    offset_count = math.ceil(num_imgs_required / num_imgs_per_transaction)

    url_list = []
    correspondence_table = {}

    subscription_key = os.environ['BING_IMAGE_SEARCH_API_KEY']
    endpoint = 'https://api.bing.microsoft.com/v7.0/images/search/'

    headers = {
    "Ocp-Apim-Subscription-Key": subscription_key,
    "Accept": "application/json"
}

    for offset in range(offset_count):
        imgs_left = num_imgs_required - offset * num_imgs_per_transaction
        imgs_to_request = min(imgs_left, num_imgs_per_transaction)
        params = {
            'q': '点字ブロック',
            'count': imgs_to_request, # Adjusting the number of images to request
            'offset': offset * num_imgs_per_transaction,
            'mkt': 'ja-JP'
        }

        try:
            # Bing Image Search APIのエンドポイントにリクエストを送信
            response = requests.get(endpoint, headers=headers, params=params)
            response.raise_for_status()  # HTTPErrorを確認
            search_results = response.json()
            values = search_results.get('value', [])
            for value in values:
                unquoted_url = urllib.parse.unquote(value['contentUrl'])
                url_list.append(unquoted_url)
        except Exception as err:
            print(f"Error occurred: {err}")

    for url in url_list:
        try:
            img_path = make_img_path(save_dir_path, url, correspondence_table)
            image = download_image(url)
            save_image(img_path, image)
            print('saved image... {}'.format(url))
        except Exception as err:
            print(f"Error occurred: {err}")

    correspondence_table_path = os.path.join(save_dir_path, 'corr_table')
    make_dir(correspondence_table_path)

    with open(os.path.join(correspondence_table_path, 'corr_table.json'), mode='w') as f:
        json.dump(correspondence_table, f)
