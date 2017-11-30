import cv2
from grid import *
import os.path

import os, errno


def capturedata():
    data_path = "data_generated"
    image_path = "images"
    try:
        os.makedirs(data_path + "/" + image_path)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    print "Press 'q' to stop recording data"
    OUTPUT_SIZE = 64
    cap = cv2.VideoCapture(0)
    cap.set(3, 640) #WIDTH
    cap.set(4, 480) #HEIGHT

    face_cascade = cv2.CascadeClassifier('models/haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier('models/haarcascade_eye.xml')

    # run grid
    # from threading import Thread
    # thread = Thread(target = run, args = (330, ))
    # thread.start()    

    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Our operations on the frame come here
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        #print(len(faces))
        # Display the resulting frame
        maxArea = 0  
        x = 0  
        y = 0  
        w = 0  
        h = 0
        facedata = None

        for (x,y,w,h) in faces:
            if (w * h > maxArea):
                maxArea = w * h
                facedata = (x, y, w, h)

        # Skip if no face
        if facedata is None:
            continue

        (x, y, w, h) = facedata
        cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]

        left = gray[y:y+h, x:x+w/2]
        right = gray[y:y+h, x+w/2:x+w]
        eyes_l = eye_cascade.detectMultiScale(left, minSize=(30, 30))
        eyes_r = eye_cascade.detectMultiScale(right, minSize=(30, 30))


        if(len(eyes_l) > 0 and len(eyes_r) > 0):
            print "Eyes found"
            (ex0,ey0,ew0,eh0) = eyes_l[0]
            (ex1,ey1,ew1,eh1) = eyes_r[0]
            eye0 = left[ey0:ey0+eh0, ex0:ex0+ew0]
            eye1 = right[ey1:ey1+eh1, ex1:ex1+ew1]

            eye0 = cv2.resize(eye0, (OUTPUT_SIZE, OUTPUT_SIZE)) 
            eye1 = cv2.resize(eye1, (OUTPUT_SIZE, OUTPUT_SIZE)) 

            cv2.imshow('eye0', eye0)
            cv2.imshow('eye1', eye1)
            if os.path.isfile('current_grid'):
                with open('current_grid') as f: 
                    current_grid = f.read()
                    import time
                    fname = str(int(time.time()))
                    left_name = data_path + '/' + image_path + '/left_' + fname + '.png'
                    right_name = data_path + '/' + image_path + '/right_' + fname + '.png'
                    with open(data_path + '/log.txt', 'a') as logfile:
                        logfile.write("%s,%s,%s\n" % (left_name, right_name, current_grid))
                        cv2.imwrite(left_name, eye0)
                        cv2.imwrite(right_name, eye1)

        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    from multiprocessing import Process
    p = Process(target=run)
    p.start()
    capturedata()
    p.join()
