import cv2 as cv


white = (255, 255, 255)
black = (24, 24, 24)
yellow = (0, 255, 255)

threshold = 500000

buttons = [
    {
        'action': 'Show Img',
        'textPos': (420, 87),
        'vertexA': (400, 50),
        'vertexB': (640, 120),
        'index': 0
    },
    {
        'action': 'Show Video',
        'textPos': (420, 187),
        'vertexA': (400, 150),
        'vertexB': (640, 220),
        'index': 1
    },
    {
        'action': 'Show Video \nFrom YT',
        'textPos': (420, 287),
        'vertexA': (400, 250),
        'vertexB': (640, 320),
        'index': 2
    }
]

def reset(sum):
    for i in range(len(sum)):
        sum[i] = 0

def reshape(img):
    shape = img.shape
    width = 800
    height = int(width * (img[0] / img[1]))

    return cv.resize(img, (width, height))

def showImg():
    img = cv.imread('./assets/i_am_suck.webp')
    cv.imshow('Img', reshape(img))
    cv.waitKey()
    cv.destroyWindow('Img')

def showVideo(link):
    capture = cv.VideoCapture(link)
    while True:
        ret, frame = capture.read()

        if ret:
            cv.imshow(reshape(frame))
        else:
            break

        if cv.waitKey(1) == ord('q'):
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
                showImg()
            elif chosen == 2:
                showVideo('./assets/hotpot.mp4') 
        keyboard = cv.waitKey(1)
        if keyboard == ord('q'):
            break


if __name__ == '__main__':
    main()