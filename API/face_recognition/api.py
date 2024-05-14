import json
import face_recognition


def search_face_recognition(img_path = "/home/ns/Homework/Face/2021302191536-聂森.png"):
    
    res = {}
    # loading
    with open("/home/ns/Homework/Face/API/face_recognition/class_list.json", "r") as file:
        class_list = json.load(file)

    with open("/home/ns/Homework/Face/API/face_recognition/name_list.json", "r") as file:
        name_list = json.load(file)

    # encoding
    unknown_image = face_recognition.load_image_file(img_path)
    unknown_encoding = face_recognition.face_encodings(unknown_image)[0]

    # compare
    distances = face_recognition.face_distance(class_list, unknown_encoding)
    best_match_index = distances.argmin()

    name = name_list[best_match_index]
    
    id_name = name.split('.')[0]  # 去除文件后缀
    id_number, real_name = id_name.split('-')  # 根据'-'分割学号和姓名
    res['user_id'] = real_name
    res['distances'] = distances[best_match_index]
    res['score'] = 1 - distances[best_match_index]

    print(f"识别为：{name}")
    return res

