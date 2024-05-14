from PIL import Image
from transformers import ViTFeatureExtractor, ViTForImageClassification
from transformers import pipeline

def gender_age_expression_live(img_path, response):
    
    img = Image.open(img_path).convert('RGB')
    model = ViTForImageClassification.from_pretrained('nateraw/vit-age-classifier')
    transforms = ViTFeatureExtractor.from_pretrained('nateraw/vit-age-classifier')
    inputs = transforms(img, return_tensors='pt')
    output = model(**inputs)
    proba = output.logits.softmax(1)
    preds = proba.argmax(1)
    response['age'] = preds
    
    age = response['age']
    if age == 0:
        response['age']= "0-10"
    elif age == 1:
        response['age'] = "10-20"
    elif age ==2:
        response['age'] = "20-30"
    elif age == 3:
        response['age'] = "30-40"
    else:
        response['age'] = "40-50"


    gender_pipe = pipeline("image-classification", model="rizvandwiki/gender-classification")
    gender_out = gender_pipe(img)
    print(gender_out[0]['label'])
    response['gender']=gender_out[0]['label']
    
    expression_pipe = pipeline("image-classification", model="trpakov/vit-face-expression")
    expression_out = expression_pipe(img)
    print(expression_out[0]['label'])
    response['expression']=expression_out[0]['label']
    
    live_pipe = pipeline("image-classification", model="venuv62/autotrained_spoof_detector")
    live_out = live_pipe(img)
    print(live_out)
    if live_out[0]['label'] == 'real':
        response['live'] = live_out[0]['score']
    else :
        response['live'] = live_out[1]['score']
    
    live = response['live']
    if (float(live) < 0.5):
        live_pass = "UNPASS"
        response['livepass'] = live_pass
    else:
        live_pass = "PASS"
        response['livepass'] = live_pass
    
    return response