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


def is_list_in_alphabetic_order(list):
    pass


def is_list_low_to_high(elements:list):
    is_low_to_high_order = True
    for i in range(len(elements)):
        elements[i] = float(elements[i].replace('$', ''))
    print(elements)
    for i in range(len(elements)-1):
        if elements[i] > elements[i+1]:
            is_low_to_high_order = False
            break
    return is_low_to_high_order


if __name__ == '__main__':
    new_list = ['$49.99', '$29.99', '$15.99', '$15.99', '$9.99', '$7.99']
    # new_list = ['$7.99', '$9.99']
    # new_list = ['7.99', '9.99', '15.99', '15.99', '29.99', '49.99']
    print(is_list_low_to_high(new_list))