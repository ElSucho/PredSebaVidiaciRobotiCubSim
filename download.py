print('please, wait...')
import requests
import os
import zipfile
import io

def download_and_save(url,path):
    if os.path.exists(path):
        return
    print("downloading",path)
    response = requests.get(url)
    open(path,"wb").write(response.content)
    print(path,"downloaded")
    
def download_Yolo3_model():
    download_and_save("http://dl.dropboxusercontent.com/scl/fi/f9m02my5iq16t1ehen6tq/yolov3.weights?rlkey=u8qoao2fgofpyspqx72hjl9wg&st=fu8nxu8u&dl=0","Yolo/yolov3.weights")

def download_emotion_model():
    download_and_save("https://drive.google.com/uc?export=download&id=115CKUF5561rzI8lYYwEQeXlL_xetWGk4","models/emotions/VGG_S_rgb/EmotiW_VGG_S.caffemodel")

def download_age_model():
    download_and_save("https://drive.google.com/uc?export=download&id=1QyJetIU3AJeO92HwEpgBIhzLrOG8-nfc","models/age/age_net.caffemodel")



def download_all():
    download_age_model()
    download_Yolo3_model()
    download_emotion_model()


if __name__ == "__main__":
    download_all()
    print("done")