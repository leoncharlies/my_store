import cv2

def main():
    while True:
        ret, frame = cap.read()
        img=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        cv2.imshow('img', img)
        cv2.imshow('frame', frame)
        input = cv2.waitKey(20)
        if input ==ord('q'):
            break
if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    width,height=1280,960
    cap.set(cv2.CAP_PROP_FRAME_WIDTH,width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT,height)
    main()

    cap.release()
    cv2.destroyAllWindows()
    
