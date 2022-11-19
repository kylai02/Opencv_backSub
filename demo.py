import cv2 as cv


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

        cv.imshow('Frame', frame)
        cv.imshow('FG Mask', fgMask)

        keyboard = cv.waitKey(1)
        if keyboard == ord('q'):
            break


if __name__ == '__main__':
    main()