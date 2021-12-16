import cv2
import numpy as np
import glob


def BlurFilter(img):
    blur = cv2.blur(img,(10,10))
    cv2.imshow("Blur Filter", blur)

def ImgDot(img):
    size = img.shape
    return_info = np.zeros(size, dtype=np.uint8)

    STEP = 4
    JITTER = 3
    RADIUS = 4

    xrange = np.arange(0, size[0]-STEP, STEP) + STEP // 2
    yrange = np.arange(0, size[1]-STEP, STEP) + STEP // 2

    np.random.shuffle(xrange)
    for i in xrange:
        np.random.shuffle(yrange)
        for j in yrange:
            x = i + np.random.randint((2 * JITTER) - JITTER + 1)
            y = j + np.random.randint((2 * JITTER) - JITTER + 1)
            color = img[x, y]
            return_info = cv2.circle(return_info, (y, x), RADIUS, (int(color[0]), int(color[1]), int(color[2])), -1, lineType=cv2.LINE_AA)

    return return_info

def NewFilter(img):
    img_gray = cv2.imread(img, cv2.COLOR_BGR2GRAY)


def Edge(img, fundo, fator=20):
    return_info = fundo.copy()

    for i in range(6, 0, -1):
        pontos = cv2.Canny(img, i*fator, i*fator*3)
        pontos = np.where(pontos != 0)
        coordinates = zip(pontos[0], pontos[1])

        for p in coordinates:
            color = img[p]
            return_info = cv2.circle(return_info, (p[1], p[0]), i,  (int(color[0]), int(color[1]), int(color[2])), -1, lineType=cv2.LINE_AA)

    return return_info

def SketchFilter(image):
    img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    img_gray_blur = cv2.GaussianBlur(img_gray, (5,5), 0)
    canny_edges = cv2.Canny(img_gray_blur, 10, 70)
    ret, mask = cv2.threshold(canny_edges, 70, 255, cv2.THRESH_BINARY_INV)
    return mask

def SharpenFilter(img):
    sharpenKernel = np.array(([[0, -1, 0], [-1, 9, -1], [0, -1, 0]]), np.float32)/9
    return cv2.filter2D(src=img, kernel=sharpenKernel, ddepth=-1)

def GreenTracking(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_blue = np.array([40,20,50])
    upper_blue = np.array([200,255,255])
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    return cv2.bitwise_and(img,img, mask= mask)

print("Choose Image or Video\n0 for image\n1 for video")
choice = int(input())

while(choice != 0 and choice != 1):
    print("Please choose 0 for image or 1 for video")
    choice = int(input())

if (choice == 0):
    img = cv2.imread(r'lenna.jpg')
    if not img.data:
        print("Could not get image")
    
    print("Choose your filter:\n0 - blur\n1 - canny dots\n2 - sketch\n3 - sharpen")
    choice_filter = int(input())
    while(choice_filter != 0 and choice_filter != 1 and choice_filter != 2 and choice_filter != 3):
        print("Please choose 0 for blur or 1 for canny dots, 2 for sketch, 3 for sharpened image")
        choice_filter = int(input())
    if choice_filter == 0:
        BlurFilter(img)
    elif choice_filter == 1:
        cv2.imshow('canny dots image', Edge(img, ImgDot(img)))
    elif choice_filter == 2:
        cv2.imshow('sketch of image', SketchFilter(img))
    else:
        cv2.imshow('sharpen filter', SharpenFilter(img))
    cv2.waitKey()
else:
    print("Choose your filter:\n0 - green tracker\n1 - grayscale\n2 - sketch\n3 - sharpen")
    choice_filter = int(input())
    while(choice_filter != 0 and choice_filter != 1 and choice_filter != 2 and choice_filter != 3):
        print("Please choose 0 for green tracker or 1 for grayscale, 2 for sketch, 3 for sharpened image")
        choice_filter = int(input())
    
    cap = cv2.VideoCapture('Bird_vid.mp4')
    
    if not cap.isOpened():
        print('Falha ao abrir o video.')
        exit(-1)
    discard = 0
    while True:
        ret, frame = cap.read()
        if ret:
            if discard == 0:
                if choice_filter == 0:
                    cv2.imshow("Green tracking", GreenTracking(frame))
                elif choice_filter == 1:
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    cv2.imshow("Gray Scaled Video", frame)
                elif choice_filter == 2:
                    cv2.imshow('sketch of Video', SketchFilter(frame))
                else:
                    cv2.imshow('sharpen filter Video', SharpenFilter(frame))
        else:
            cap = cv2.VideoCapture('Bird_vid.mp4')
        key = cv2.waitKey(15)
        if key == 27:
            break
    cap.release()
    cv2.destroyAllWindows()
