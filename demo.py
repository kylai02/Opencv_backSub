import cv2 as cv


white = (255, 255, 255)
black = (0, 0, 0)

buttons = [
    {
        'action': 'Show Img',
        'textPos': (400, 35),
        'vertexA': (400, 10),
        'vertexB': (650, 50)
    }
]

def main():
    # Set up camera
    capture = cv.VideoCapture(0)
    if not capture.isOpened():
        print('Unable to open camera.')
        exit(0)

    backSub = cv.createBackgroundSubtractorMOG2()
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
            cv.putText(frame, button['action'], button['textPos'], cv.FONT_HERSHEY_SIMPLEX, 1, white)

        cv.imshow('Frame', frame)
        cv.imshow('FG Mask', fgMask)

        keyboard = cv.waitKey(1)
        if keyboard == ord('q'):
            break


if __name__ == '__main__':
    main()