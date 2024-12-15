from ultralytics import YOLO
import torch

model = YOLO('yolov8m.pt')
if __name__ == '__main__':
    model.train(data='D:\\Code\YOLO\\plate_char\\data.yaml', epochs=45, imgsz=640,workers=1,batch=5,device=0)
    model.val() 
    # print(torch.cuda.is_available())  # Should return True
    # print(torch.cuda.device_count())  # Number of GPUs available