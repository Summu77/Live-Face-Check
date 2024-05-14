# Live-Face-Check
Online class check-in system, Face recognition, Liveness detection.

The class check-in and sign-in system is the final assignment for the content security experimental course of  Wuhan University, which supports face detection, liveness detection, age detection, gender detection, and expression detection of various schemes.

Developer: Nie Sen, Wuhan University

Contact me: niesen@whu.edu.cn

## Screenshots

![image-20240514180630550](D:\桌面\face2\Live-Face-Check\assets\image-20240514180630550.png)

![image-20240514181131232](D:\桌面\face2\Live-Face-Check\assets\image-20240514181131232.png)

![1715681651677](D:\桌面\face2\Live-Face-Check\assets\1715681651677.png)

![image-20240514181542615](D:\桌面\face2\Live-Face-Check\assets\image-20240514181542615.png)

## Requirement

Please pip/conda install the following library:

- pytorch
- transfomers
- baidu-aip
- face_recognition
- facenet_pytorch
- Flask

For all the above library files, please select the latest one based on the CUDA version.

Some of the HuggingFace models need to be used, but don't worry if you don't have a problem with your network, and if your network is not accessible, please download it in advance.

The following HuggingFace models are used：

- rizvandwiki/gender-classification
- trpakov/vit-face-expression
- venuv62/autotrained_spoof_detector
- nateraw/vit-age-classifier

If you don't download the above models, then methods 2 and 3 will not be available.

## Quick start

The system is built on Flask, which is simple and easy to use, and you can quickly start the project by following the following four steps:

1. Git clone the entire project
2. Please register a Baidu API account and modify the api.py and register.py files in the Baidu folder.
3. Use the register function I provided to complete the registration of class members
4. Run app.py file to experience the system online

If you have any suggestions, please feel free to contact me!

If you want to add, remove, or replace methods, please modify the API folder!
## More Info about Method

Still updating...

