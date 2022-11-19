import cv2 as cv


white = (255, 255, 255)
black = (24, 24, 24)
yellow = (0, 255, 255)

threshold = 500000

buttons = [
    {
        'action': 'I am suck',
        'textPos': (520, 87),
        'vertexA': (500, 50),
        'vertexB': (640, 120),
        'index': 0
    },
    {
        'action': 'Cry Dog',
        'textPos': (520, 187),
        'vertexA': (500, 150),
        'vertexB': (640, 220),
        'index': 1
    },
    {
        'action': 'Hotpot',
        'textPos': (520, 287),
        'vertexA': (500, 250),
        'vertexB': (640, 320),
        'index': 2
    },
    {
        'action': 'Rick Roll',
        'textPos': (520, 387),
        'vertexA': (500, 350),
        'vertexB': (640, 420),
        'index': 3
    }
]

def reset(sum):
    for i in range(len(sum)):
        sum[i] = 0

def reshape(img):
    shape = img.shape
    width = 800
    height = int(width * (shape[0] / shape[1]))

    return cv.resize(img, (width, height))

def showImg(link):
    img = cv.imread(link)
    cv.imshow('Image', reshape(img))
    cv.waitKey()
    cv.destroyWindow('Image')

def showVideo(link):
    capture = cv.VideoCapture(link)
    while True:
        ret, frame = capture.read()

        if ret:
            cv.imshow('Video', reshape(frame))
        else:
            break

        if cv.waitKey(20) == ord('z'):
            break
    


def main():
    # Set up camera
    capture = cv.VideoCapture(0)
    if not capture.isOpened():
        print('Unable to open camera.')
        exit(0)

    backSub = cv.createBackgroundSubtractorMOG2()
    sum = [0, 0, 0, 0]
    ctr = 0

    while True:
        ret, frame = capture.read()
        if frame is None:
            break

        fgMask = backSub.apply(frame)
        frame = cv.flip(frame, 1)
        fgMask = cv.flip(fgMask, 1)

        # Add button to the frame
        for button in buttons:
            cv.rectangle(frame, button['vertexA'], button['vertexB'], black, -1)
            cv.putText(frame, button['action'], button['textPos'], cv.FONT_HERSHEY_COMPLEX_SMALL, 0.8, yellow)
        
        cv.imshow('Frame', frame)
        cv.imshow('FG Mask', fgMask)
        
        for button in buttons:
            a, b = button['vertexA'], button['vertexB']
            for i in range(a[1], b[1]):
                for j in range(a[0], b[0]):
                    sum[button['index']] += fgMask[i][j]

        ctr += 1
        chosen = -1
        if ctr >= 24:
            for i, value in enumerate(sum):
                if value >= threshold:
                    if chosen == -1:
                        chosen = i
                    else:
                        chosen = -1
                        reset(sum)
            reset(sum)
                 
        if not chosen == -1:
            print(chosen)
            if chosen == 0:
                showImg('./assets/i_am_suck.webp')
            elif chosen == 1:
                showImg('./assets/cry.png')
            elif chosen == 2:
                showVideo('./assets/hotpot.mp4') 
            elif chosen == 3:
                showVideo('./assets/rick_roll.mp4')

        keyboard = cv.waitKey(1)
        if keyboard == ord('q'):
            break


if __name__ == '__main__':
    main()