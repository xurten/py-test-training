import os
from PIL import Image


def sum_list_of_strings(number_list):
    count = 0
    for element in number_list:
        count = count + int(element)
    return str(count)


def remove_html_tags_from_string(message: str):
    import re
    html_regex = re.compile('<.*?>')
    text_without_html = re.sub(html_regex, '', message)
    return text_without_html


def download_picture_from_url(url_path: str, picture_name='new_picture.jpg'):
    import urllib.request
    print(url_path)
    try:
        urllib.request.urlretrieve(url_path, picture_name)
    except Exception as e:
        print(f"Exception with retrieving of file {e}")


def validate_picture(picture_path):
    image = Image.open(picture_path)
    width, height = image.size
    picture_size = os.path.getsize(picture_path)
    print(f"{width} {height} {picture_size}")
    assert width > 0
    assert height > 0
    assert picture_size > 0


def remove_file(file_path):
    os.remove(file_path)