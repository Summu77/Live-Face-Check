import face_recognition
import os
import json
import numpy as np

folder_path = '/home/ns/Homework/Face/class1'

class_list = []
name_list = []

for filename in os.listdir(folder_path):
    
    image_path = os.path.join(folder_path, filename)
    if not filename.lower().endswith(('.png', '.jpg')):
        continue  
    
    try:
        current_image = face_recognition.load_image_file(image_path)
        current_encoding = face_recognition.face_encodings(current_image)[0]
        name_list.append(filename)
        class_list.append(current_encoding)
        print(f"{filename} SUCCESS!")
        
    except Exception as e:
        print(f"{filename} FAIL!")

print("Finised encoding!")

class_list = [arr.tolist() for arr in class_list]
with open("/home/ns/Homework/Face/API/face_recognition/class_list.json", "w") as file:
    json.dump(class_list, file)

with open("/home/ns/Homework/Face/API/face_recognition/name_list.json", "w") as file:
    json.dump(name_list, file)
    
print("Finised register!")
