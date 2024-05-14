import os
from aip import AipFace
import base64
import time 

APP_ID = "XXXX"
API_KEY = "XXXX"
SECRET_KEY = 'XXXX'
client = AipFace(APP_ID, API_KEY, SECRET_KEY)

image_folder = '/home/ns/Homework/Face/class1'
group_id = 'class1'


for image_filename in os.listdir(image_folder):
    if image_filename.lower().endswith(('.jpg', '.png')):
        image_path = os.path.join(image_folder, image_filename)
        
        # 读取图片内容并进行Base64编码
        with open(image_path, 'rb') as image_file:
            image_data = base64.b64encode(image_file.read()).decode('utf-8')

        # 例如：2020302171027-黄鑫奥.png 中的 "2020302171027" 是用户ID  
        user_id = image_filename.rsplit('-', 1)[0]

        
        result = client.addUser(image_data, 'BASE64', group_id, user_id)
        print(result)
        
        # API
        time.sleep(1)


print("人脸注册完成。")