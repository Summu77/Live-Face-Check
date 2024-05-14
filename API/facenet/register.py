import os
from PIL import Image
from facenet_pytorch import MTCNN, InceptionResnetV1
import torch
import json


# 初始化 MTCNN 和 InceptionResnetV1
mtcnn = MTCNN(image_size=160, margin=0, min_face_size=20, keep_all=True)
resnet = InceptionResnetV1(pretrained='vggface2').eval()


def get_face_embeddings(folder_path):
    embeddings_list = []
    name_list = []
    # 遍历文件夹中的所有文件
    for img_file in os.listdir(folder_path):
        # 确保只处理图像文件
        if img_file.lower().endswith(('.png', '.jpg')):
            
            img_path = os.path.join(folder_path, img_file)
            img = Image.open(img_path)
            
            if img.mode == 'RGBA':
                img = img.convert('RGB')
            
            # 使用 MTCNN 检测人脸
            try:
                faces = mtcnn(img)

                if faces is not None:
                    face_embeddings = resnet(faces)
                    embeddings_list.append(face_embeddings)
                    name_list.append(img_file)
                    print(f"{img_file} SUCCESS!")
                else:
                    print(f"{img_file} ERROR!")
            except Exception as e:
                print(f"{img_file} ERROR!")
                print(e)
                
    return embeddings_list, name_list


folder_path = "/home/ns/Homework/Face/class1"
face_embeddings, name_list = get_face_embeddings(folder_path)

# 输出
print("Extracted face embeddings count:", len(face_embeddings))

class_list = [arr.tolist() for arr in face_embeddings]
with open("/home/ns/Homework/Face/API/facenet/class_list.json", "w") as file:
    json.dump(class_list, file)
    
with open("/home/ns/Homework/Face/API/facenet/name_list.json", "w") as file:
    json.dump(name_list, file)
    
print("Finised register!")
    
    
