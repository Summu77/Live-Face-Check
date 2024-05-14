from facenet_pytorch import MTCNN, InceptionResnetV1
from PIL import Image
import torch
import json
import torch.nn.functional as F


def get_embedding(image_path, mtcnn, resnet):
    
    image = Image.open(image_path)
    # Convert RGBA to RGB if necessary
    if image.mode == 'RGBA':
        image = image.convert('RGB')
    # Detect faces
    face = mtcnn(image)
    # Calculate embedding
    with torch.no_grad():
        embedding = resnet(face)
    
    return embedding

def find_most_similar(target_embedding, class_list):
    # Ensure target_embedding is a tensor and add batch dimension
    if not isinstance(target_embedding, torch.Tensor):
        target_embedding_tensor = torch.tensor(target_embedding)
    else:
        target_embedding_tensor = target_embedding.clone().detach()
    target_embedding_tensor = target_embedding_tensor.unsqueeze(0)
    
    similarities = []
    
    for known_embedding in class_list:
        if not isinstance(known_embedding, torch.Tensor):
            known_embedding_tensor = torch.tensor(known_embedding)
        else:
            known_embedding_tensor = known_embedding.clone().detach()
        known_embedding_tensor = known_embedding_tensor.unsqueeze(0)
        
        # Compute cosine similarity over the last dimension
        similarity = F.cosine_similarity(target_embedding_tensor, known_embedding_tensor, dim=1)
        # Summing over the batch dimension to get a single value for the similarity
        summed_similarity = torch.sum(similarity)
        similarities.append(summed_similarity.item())
        
    # Find the index of the maximum similarity (most similar)
    most_similar_index = similarities.index(max(similarities))
    return similarities, most_similar_index

def search_facenet(img_path):
    
    res = {}
    # 初始化 MTCNN 和 ResNet
    mtcnn = MTCNN(image_size=160, margin=0, min_face_size=20, keep_all=True)
    resnet = InceptionResnetV1(pretrained='vggface2').eval()
    
    # Compute embedding for the target image
    target_image_path = img_path
    target_embedding = get_embedding(target_image_path, mtcnn, resnet)

    # loading
    with open("/home/ns/Homework/Face/API/facenet/class_list.json", "r") as file:
        class_list = json.load(file)

    with open("/home/ns/Homework/Face/API/facenet/name_list.json", "r") as file:
        name_list = json.load(file)

    # search
    similarities, index_of_most_similar = find_most_similar(target_embedding, class_list)
    name = name_list[index_of_most_similar]
    print(f"匹配为：{name}")
    id_name = name.split('.')[0]  # 去除文件后缀
    id_number, real_name = id_name.split('-')  # 根据'-'分割学号和姓名
    res['user_id'] = real_name
    
    
    similarities_tensor = torch.tensor(similarities)
    softmax_output = torch.softmax(similarities_tensor, dim=0)
    max_value, max_index = torch.max(softmax_output, dim=0)
    res['score'] = float(max_value)
    
    return res
