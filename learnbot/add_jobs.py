import pytesseract
from PIL import Image
import json
import os
import string
import re

def list_files(directory):
    for file in os.listdir(directory):
        print(file)

def add_job(user, data_file, new_job):
    with open(data_file, 'r') as f:
        data = json.load(f)
    
    try:
        data[user]['jobs'].append(new_job)
    except:
        data[user] = {"coins": 0.0, "current": 0, "voice": "en-US-ChristopherNeural", "jobs": []}
        data[user]['jobs'].append(new_job)
    
    with open(data_file, 'w') as f:
        json.dump(data, f)

def ocr_from_image(image_path):
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)
    return text

images_path = "images/"
data_file = "data.json"
user = input("Insert user ID: ")
lang = input("Insert Job name: ")
target_score = input("Insert target score: ")
target_score = float(target_score)
difficulty = input("Insert difficulty: ")
difficulty = float(difficulty)

list_images = os.listdir(images_path)
list_images.sort()

for i in list_images:
    text = ocr_from_image(images_path + i).replace('\n', ' ')
    text_list = text.split('.')
    text_list.pop(-1)
    for j in text_list:
        if j != "":
            new_job = {"lang": lang, "text": j.lstrip(), "target_score": target_score, "current_score": 0.0, "difficulty": difficulty}
            add_job(user, data_file, new_job)
