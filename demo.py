import cv2 as cv


white = (255, 255, 255)
black = (24, 24, 24)
yellow = (0, 255, 255)

threshold = 50000

buttons = [
    {
        'action': 'Show Img',
        'textPos': (420, 45),
        'vertexA': (400, 10),
        'vertexB': (600, 80),
        'index': 0
    },
    {
        'action': 'Show Video',
        'textPos': (420, 145),
        'vertexA': (400, 110),
        'vertexB': (600, 180),
        'index': 1
    },
    {
        'action': 'Show Video From YT',
        'textPos': (420, 245),
        'vertexA': (400, 210),
        'vertexB': (600, 280),
        'index': 2
    }
]

def reset(sum):
    for i in range(len(sum)):
        sum[i] = 0

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
            cv.putText(frame, button['action'], button['textPos'], cv.FONT_HERSHEY_TRIPLEX, 1, yellow)
        
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
                img = cv.imread('./assets/i_am_suck.webp')
                cv.imshow('Img', img)
                cv.waitKey()
                cv.destroyWindow('Img')

        keyboard = cv.waitKey(1)
        if keyboard == ord('q'):
            break


if __name__ == '__main__':
    main()