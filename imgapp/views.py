
from django.http import HttpResponse
from django.shortcuts import render
from django.http import StreamingHttpResponse

import torch
import json
model = torch.hub.load('./yolov5', 'custom', path='./yolov5/runs/train/exp2/weights/best.pt', source='local')

import cv2
# Create your views here.
def img(request):
    return render(request,"image.html")


def stream():


    vid = cv2.VideoCapture("./inference-tests/test_img2.jpg")
    while (True):

        # Capture the video frame
        # by frame
        ret, frame = vid.read()
        results = model(frame)

        boxes = results.pandas().xyxy[0].to_json(orient="records")
        boxes = json.loads(boxes)
        print(boxes)



        for box in boxes:

            print(box)
            print(box['xmin'])
            pointA = (int(box['xmin']), int(box['ymin']))
            pointB = (int(box['xmax']), int(box['ymax']))
            print(pointA)
            if (box['name'] == 'helmet'):
                conf = round(box['confidence'] * 100)
                outputtext = "helmet" + " " + str(conf) + "%"
                cv2.putText(frame, text=outputtext, org=(pointA), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=1,
                            color=(0, 255, 0), thickness=1)
                cv2.rectangle(frame, pointA, pointB, (0, 255, 0), 3)
            else:
                conf = round(box['confidence'] * 100)
                outputtext2 = "no_helmet" + " " + str(conf) + "%"

                cv2.putText(frame, text=outputtext2, org=(pointA), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=1,
                            color=(255, 0, 0), thickness=1)
                print("reached")
                cv2.rectangle(frame, pointA, pointB, (255, 0, 0), 3)
        if not ret:
            print("Error")

        # Display the resulting frame
        image_bytes = cv2.imencode('.jpg', frame)[1].tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + image_bytes + b'\r\n')

        # the 'q' button is set as the
        # quitting button you may use any
        # desired button of your choice


    # After the loop release the cap object
    vid.release()
    cv2.destroyAllWindows()


def img_feed(request):
    print ("hai")
    return StreamingHttpResponse(stream(), content_type='multipart/x-mixed-replace;boundary=frame')



