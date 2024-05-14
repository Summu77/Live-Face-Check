# https://ai.baidu.com/ai-doc/FACE/ek37c1qiz#%E4%BA%BA%E8%84%B8%E6%A3%80%E6%B5%8B

from aip import AipFace
import base64
import json
def search_baidu(image_path):
    
    response = {}
    
    APP_ID = "XXXX"
    API_KEY = "XXXX"
    SECRET_KEY = 'XXXX'
    client = AipFace(APP_ID, API_KEY, SECRET_KEY)
    
    # 读取图片内容并进行Base64编码
    with open(image_path, 'rb') as image_file:
        image_data = base64.b64encode(image_file.read()).decode('utf-8')  

    imageType = "BASE64"
    groupIdList = "class1"
    result = client.search(image_data, imageType, groupIdList);
    print(result)

    if result['error_msg'] == 'SUCCESS':
        
        user_id = result['result']['user_list'][0]['user_id']
        score = result['result']['user_list'][0]['score']
        print(f"SUCCESS! \nuser_id:{user_id}")
        
        input_file = '/home/ns/Homework/Face/API/baidu/id_to_name_mapping.json'
        with open(input_file, 'r') as json_file:
            id_to_name_mapping = json.load(json_file)
            
        response['user_id'] = id_to_name_mapping[user_id]
    
        response['score'] = score
        
        # 活体+ 表情 + 年龄 + 性别 检测 
        options = {}
        options["face_field"] = "age,expression,gender"
        options["max_face_num"] = 2
        options["liveness_control"] = "LOW"
        res = client.detect(image_data, imageType, options)
        
        if res['error_msg'] == 'SUCCESS':
            
            base = res['result']['face_list'][0]
            live = base['liveness']['livemapscore']
            age = base['age']
            expression = base['expression']['type']
            gender = base['gender']['type']
            
            response['live'] = live
            response['age'] = age
            response['expression'] = expression
            response['gender'] = gender
            
            print(f"age:{age} expression:{expression} gender:{gender}")
            
            if (float(live) < 0.6):
                print(f"The liveness test failed! live:{live} < 0.6")
                live_pass = "UNPASS"
                response['livepass'] = live_pass
            else:
                print(f"The liveness test passed! live:{live} > 0.6 ")
                live_pass = "PASS"
                response['livepass'] = live_pass
        
    else:
        user_id = -1
        response['user_id']="None"
        print(f"ERROR! user_id:{user_id}")
    
    return response

